$(document).ready(function () {
    var selectedMedications = [];

    $("#medicamento").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "/autocomplete",
                dataType: "json",
                data: {
                    term: request.term
                },
                success: function (data) {
                    response(data.map(function (item) {
                        return {
                            label: item.substancia || item.produto,
                            value: item.substancia || item.produto,
                            laboratorio: item.laboratorio,
                            produto: item.produto,
                            substancia: item.substancia,
                            apresentacao: item.apresentacao
                        };
                    }));
                }
            });
        },
        minLength: 2,
        select: function (event, ui) {
            addMedicationToList(ui.item);
            $(this).val('');  // Clear the input field
            return false;  // Prevent the default behavior of setting the value to the selected item
        }
    }).data("ui-autocomplete")._renderItem = function (ul, item) {
        return $("<li>")
            .append("<div><span class='medicamento'>" + (item.substancia || item.produto) + ", " + item.apresentacao + "</span><br><span class='descricao'>" + item.laboratorio + "</span></div>")
            .appendTo(ul);
    };

    function addMedicationToList(item) {
        selectedMedications.push(item);
        const listItem = $("<li>").text(item.label + ", " + item.apresentacao + " (" + item.laboratorio + ")");
        $("#medication-list").append(listItem);
    }

    $("#generate-prescription").on("click", function () {
        $.ajax({
            type: "POST",
            url: "/generate_prescription",
            contentType: "application/json",
            data: JSON.stringify({ medications: selectedMedications }),
            success: function (response) {
                window.open(response.url, '_blank');
            }
        });
    });
});
