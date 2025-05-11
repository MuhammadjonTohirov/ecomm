(function(django) {
    const $ = django.jQuery;
    
    $(document).ready(function() {
        // Function to update employee dropdown based on selected organization
        function updateEmployeeDropdown() {
            const organizationId = $('#id_organization').val();
            const currentEmployeeId = $('#id_employee').val(); // Get current selection
            
            if (organizationId) {
                // Disable employee dropdown while loading
                $('#id_employee').prop('disabled', true);
                
                // Fetch employees for the selected organization
                $.ajax({
                    url: '/crm/api/get_employees_by_organization/',
                    data: {'organization_id': organizationId},
                    dataType: 'json',
                    success: function(data) {
                        // Store current selection
                        const selectedValue = $('#id_employee').val();
                        
                        // Clear current options
                        $('#id_employee').empty();
                        
                        // Add empty option
                        $('#id_employee').append($('<option></option>').attr('value', '').text('---------'));
                        
                        // Add new options
                        $.each(data.employees, function(i, employee) {
                            $('#id_employee').append($('<option></option>')
                                .attr('value', employee.id)
                                .text(employee.name));
                        });
                        
                        // Restore previously selected value if it exists in the new options
                        if (selectedValue) {
                            $('#id_employee').val(selectedValue);
                        }
                        
                        // Re-enable dropdown
                        $('#id_employee').prop('disabled', false);
                    }
                });
            } else {
                // If no organization selected, empty employee dropdown
                // But only if we're not editing an existing record
                if (!currentEmployeeId) {
                    $('#id_employee').empty().prop('disabled', true);
                    $('#id_employee').append($('<option></option>').attr('value', '').text('---------'));
                }
            }
        }
        
        // Only trigger the update when organization changes
        $('#id_organization').change(updateEmployeeDropdown);
        
        // Only run the initialization if organization is selected but employee is empty
        if ($('#id_organization').val() && !$('#id_employee').val()) {
            updateEmployeeDropdown();
        }
    });
})(django);