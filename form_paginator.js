$(document).ready(function () {
    // Function to handle showing fields one by one
    function showFieldsSequentially(formId) {
        const $form = $(formId);
        const $fields = $form.find('.form-group');
        let currentFieldIndex = 0;

        // Show the first field
        $($fields[currentFieldIndex]).show();

        // Function to show the next field
        function showNextField() {
            if (currentFieldIndex < $fields.length - 1) {
                currentFieldIndex++;
                $($fields[currentFieldIndex]).fadeIn();
            }
        }

        // Attach event listeners to each input field to show the next field on input
        $fields.each(function (index, field) {
            const $input = $(field).find('input');
            $input.on('input', function () {
                // Check if the current input is valid
                if (this.checkValidity()) {
                    showNextField();
                }
            });
        });
    }

    // Initialize the function for the specific form
    showFieldsSequentially('#dynamic-form');
});
