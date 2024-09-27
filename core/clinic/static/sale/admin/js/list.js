var tblSale;
var input_date_range;
var select_type_sale;
var sale = {
    list: function (all) {
        var parameters = {
            'action': 'search',
            'type_sale': select_type_sale.val(),
            'start_date': input_date_range.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_date_range.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        tblSale = $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: ""
            },
            columns: [
                {data: "number"},
                {data: "type.name"},
                {data: "employee.user.names"},
                {data: "mascot.name"},
                {data: "date_joined"},
                {data: "hour"},
                {data: "subtotal"},
                {data: "total_iva"},
                {data: "total"},
                {data: "status.name"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [1],
                    class: 'text-left',
                    render: function (data, type, row) {
                        var name = row.type.name;
                        switch (row.type.id) {
                            case 'sale':
                                return '<span class="badge badge-info badge-pill">' + name + '</span>';
                            case 'quote':
                                return '<span class="badge badge-warning badge-pill">' + name + '</span>';
                            case 'vaccine':
                                return '<span class="badge badge-success badge-pill">' + name + '</span>';
                        }
                        return '<span class="badge badge-badge-secondary badge-pill">' + name + '</span>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var name = row.status.name;
                        switch (row.status.id) {
                            case 'active':
                                return '<span class="badge badge-info badge-pill">' + name + '</span>';
                            case 'cancel':
                                return '<span class="badge badge-warning badge-pill">' + name + '</span>';
                            case 'finalized':
                                return '<span class="badge badge-success badge-pill">' + name + '</span>';
                        }
                        return '<span class="badge badge-badge-secondary badge-pill">' + name + '</span>';
                    }
                },
                {
                    targets: [-3, -4, -5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '<a class="btn btn-info btn-xs btn-flat" rel="details" data-toggle="tooltip" title="Consulta"><i class="fas fa-folder-open"></i></a> ';
                        buttons += '<a href="' + pathname + 'print/invoice/' + row.id + '/" target="_blank" data-toggle="tooltip" title="Imprimir" class="btn btn-success btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" data-toggle="tooltip" title="Eliminar" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a>';
                        return buttons;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $('[data-toggle="tooltip"]').tooltip();
                $(this).wrap('<div class="dataTables_scroll"><div/>');
                var total = json.reduce((a, b) => a + (parseFloat(b.total) || 0), 0);
                $('.total').html('$' + total.toFixed(2));
            }
        });
    }
};

$(function () {

    select_type_sale = $('select[name="type_sale"]');
    input_date_range = $('input[name="date_range"]');

    input_date_range
        .daterangepicker({
                language: 'auto',
                startDate: new Date(),
                locale: {
                    format: 'YYYY-MM-DD',
                },
                autoApply: true,
            }
        )
        .on('change.daterangepicker apply.daterangepicker', function (ev, picker) {
            sale.list(false);
        });

    $('#data tbody')
        .off()
        .on('click', 'a[rel="details"]', function () {
            $('.tooltip').remove();
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var row = tblSale.row(tr.row).data();
            var items = [];
            items.push({'id': 'Sintomas', 'name': row.symptoms});
            items.push({'id': 'Observación', 'name': row.observation});
            items.push({'id': 'Diagnóstico', 'name': row.diagnosis});
            $('#tblQuote').DataTable({
                autoWidth: false,
                destroy: true,
                data: items,
                paging: false,
                ordering: false,
                info: true,
                columns: [
                    {data: "id"},
                    {data: "name"},
                ],
                columnDefs: [
                    // {
                    //     targets: [0],
                    //     class: 'text-center',
                    //     render: function (data, type, row) {
                    //         return data;
                    //     }
                    // },
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#tblProducts').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_detail_product',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "product.name"},
                    {data: "product.category.name"},
                    {data: "price"},
                    {data: "cant"},
                    {data: "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [-1, -3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + data.toFixed(2);
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#tblVaccines').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_detail_vaccine',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "product.name"},
                    {data: "product.category.name"},
                    {data: "date_vaccine"},
                    {data: "next_date"},
                    {data: "price"},
                    {data: "cant"},
                    {data: "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [-1, -3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + data.toFixed(2);
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#tblMedicalParameter').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_historial_medical',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "medical_parameter.name"},
                    {data: "valor"},
                    {data: "description"},
                ],
                columnDefs: [
                    {
                        targets: [1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                    {
                        targets: [0],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('.nav-tabs a[href="#home"]').tab('show');
            $('#myModalDetails').modal('show');
        });

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
        sorter: function (data) {
            return data.sort(function (a, b) {
                return a.text < b.text ? -1 : a.text > b.text ? 1 : 0;
            });
        }
    });

    select_type_sale.on('change.select2', function () {
        sale.list();
    });

    $('.drp-buttons').hide();

    sale.list(false);

    $('.btnSearchAll').on('click', function () {
        sale.list(true);
    });
});
