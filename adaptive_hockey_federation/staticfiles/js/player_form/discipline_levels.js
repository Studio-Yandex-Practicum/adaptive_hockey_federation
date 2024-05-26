$("#id_discipline_name").change(function () {
    const url = $("#playerForm").attr("data-discipline-level");
    const discipline_level = $(this).val();
    $.ajax({
        url: url,
        data: {
            'discipline_level_id': discipline_level
        },
        success: function (data) {
            let html_data = '<option value="">---------</option>';
            data.forEach(function (discipline_level) {
                html_data += `<option value="${discipline_level.id}">${discipline_level.name}</option>`
            });
            $("#id_discipline_level").html(html_data);
        }
    })
})
