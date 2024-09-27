var tblTeam;

var team = {
    list: function () {
        tblTeam = $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search'
                },
                dataSrc: ""
            },
            columns: [
                {"data": "id"},
                {"data": "names"},
                {"data": "job"},
                {"data": "image"},
                {"data": "teamsocialnetworks"},
                {"data": "state"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="image" class="btn btn-secondary btn-xs btn-flat"><i class="fas fa-file-image"></i></a>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var content = '';
                        row.teamsocialnetworks.forEach(function (value, index, array) {
                            content += '<a class="badge badge-secondary badge-pill mr-2" href="' + value.url + '" target="_blank"><i class="' + value.icon + '"></i></a>';
                        });
                        return content;
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data) {
                            return '<span class="badge badge-success badge-pill">Activo</span>';
                        }
                        return '<span class="badge badge-danger badge-pill">Inactivo</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href="' + pathname + 'update/' + row.id + '/" data-toggle="tooltip" title="Editar" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" data-toggle="tooltip" title="Eliminar" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
                $('[data-toggle="tooltip"]').tooltip();
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {
    team.list();

    $('#data tbody')
        .off()
        .on('click', 'a[rel="image"]', function () {
            var tr = tblTeam.cell($(this).closest('td, li')).index();
            var data = tblTeam.row(tr.row).data();
            load_image({'url': data.image});
        });
});