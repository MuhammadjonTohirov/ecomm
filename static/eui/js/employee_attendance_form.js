(function(django) {
    const $ = django.jQuery;
    
    $(document).ready(function() {
        function updateEmployeeDropdown() {
            const organizationId = $('#id_organization').val();
            const currentEmployeeId = $('#id_employee').val();
            
            if (organizationId) {
                // Disable employee dropdown while loading
                $('#id_employee').prop('disabled', true);
                
                $.ajax({
                    url: '/crm/api/get_employees_by_organization/',
                    data: {'organization_id': organizationId},
                    dataType: 'json',
                    success: function(data) {
                        const selectedValue = $('#id_employee').val();
                        
                        // Clear and reset dropdown
                        $('#id_employee').empty()
                            .append($('<option></option>')
                            .attr('value', '')
                            .text('---------'));
                        
                        // Add employee options
                        data.employees.forEach(function(employee) {
                            $('#id_employee').append($('<option></option>')
                                .attr('value', employee.id)
                                .text(employee.name));
                        });
                        
                        // Restore selected value if it exists
                        if (selectedValue) {
                            $('#id_employee').val(selectedValue);
                        }
                        
                        $('#id_employee').prop('disabled', false);
                    },
                    error: function(xhr, status, error) {
                        console.error('Error fetching employees:', error);
                        $('#id_employee').prop('disabled', false);
                    }
                });
            } else {
                // Clear employee dropdown if no organization selected
                if (!currentEmployeeId) {
                    $('#id_employee')
                        .empty()
                        .append($('<option></option>')
                        .attr('value', '')
                        .text('---------'))
                        .prop('disabled', true);
                }
            }
        }
        
        // Bind change event to organization dropdown
        $('#id_organization').on('change', updateEmployeeDropdown);
        
        // Initialize on page load if organization is selected
        if ($('#id_organization').val() && !$('#id_employee').val()) {
            updateEmployeeDropdown();
        }
    });
})(django);