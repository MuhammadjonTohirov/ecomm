from django import forms
from crm.models.salary import EmployeeSalary
from crm.models.employee import OrganizationEmployee
from crm.models.organization import Organization

class EmployeeSalaryForm(forms.ModelForm):
    organization = forms.ModelChoiceField(queryset=Organization.objects.all(), required=True)
    
    class Meta:
        model = EmployeeSalary
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Limit organizations based on user permissions
        if self.request and not self.request.user.is_superuser:
            self.fields['organization'].queryset = Organization.objects.filter(owner__user=self.request.user)
        
        # Get the current employee if this is an existing instance
        current_employee = None
        if self.instance and self.instance.pk and hasattr(self.instance, 'employee') and self.instance.employee:
            current_employee = self.instance.employee
            
            try:
                # Get organization from employee
                org = current_employee.organization
                
                # Set initial value for organization
                self.initial['organization'] = org.pk
                
                # Make sure employee queryset includes the current employee
                self.fields['employee'].queryset = OrganizationEmployee.objects.filter(organization=org)
            except Exception as e:
                print(f"Error setting organization: {e}")
        
        # For form submissions, update the employee queryset based on selected organization
        if self.data and 'organization' in self.data:
            try:
                org_id = int(self.data.get('organization'))
                self.fields['employee'].queryset = OrganizationEmployee.objects.filter(organization_id=org_id)
            except (ValueError, TypeError):
                pass
        # If no organization selected yet but we have a current employee, ensure it's in the queryset
        elif current_employee:
            self.fields['employee'].queryset = OrganizationEmployee.objects.filter(pk=current_employee.pk)
        else:
            self.fields['employee'].queryset = OrganizationEmployee.objects.none()