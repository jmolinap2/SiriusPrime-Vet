var input_datejoined, input_hour;
var current_date;
var select_employee, select_mascot;
var fv;
var tblQuotes;
var selected_quote = {};

document.addEventListener('DOMContentLoaded', function (e) {
    fv = FormValidation.formValidation(document.getElementById('frmForm'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
                // excluded: new FormValidation.plugins.Excluded(),
            },
            fields: {
                date_joined: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    },
                },
                hour: {
                    validators: {
                        notEmpty: {
                            message: 'Debe seleccionar una hora'
                        },
                        regexp: {
                            regexp: /^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$/,
                            message: 'El formato de la hora no es el correcto'
                        },
                    },
                },
                symptoms: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                employee: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un médico'
                        },
                    }
                },
                mascot: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una mascota'
                        },
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fv.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var params = new FormData(fv.form);
            params.append('hour', input_hour.val());
            var args = {
                'content': '¿Estas seguro de agendar la siguiente cita?',
                'params': params,
                'success': function (request) {
                    alert_sweetalert({
                        'title': 'Notificación',
                        'message': request.msg,
                        'timer': 3000,
                        'callback': function () {
                            location.href = fv.form.getAttribute('data-url');
                        }
                    });
                }
            };
            submit_with_formdata(args);
        });
});

$(function () {

    input_datejoined = $('input[name="date_joined"]');
    input_hour = $('input[name="hour"]');
    current_date = new moment().format("YYYY-MM-DD");
    select_employee = $('select[name="employee"]');
    select_mascot = $('select[name="mascot"]');

    input_datejoined.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        date: current_date,
        minDate: current_date,
    });

    input_datejoined.on('change.datetimepicker', function (e) {
        fv.revalidateField('date_joined');
        input_hour.val('');
        selected_quote = {};
    });

    $('.select2').select2({
        theme: 'bootstrap4',
        language: 'es'
    });

    select_employee.on('change.select2', function () {
        fv.revalidateField('employee');
        input_hour.val('');
        if (!$.isEmptyObject(selected_quote)) {
            var cells = tblQuotes.cells().nodes();
            $(cells).find('input[type="checkbox"][name="schedule"]').prop('checked', false);
            selected_quote = {};
        }
    });

    select_mascot.on('change.select2', function () {
        fv.revalidateField('mascot');
    });

    input_datejoined.datetimepicker('date', input_datejoined.val());

    $('.btnScheduling').on('click', function () {
        $('#datecite').html(input_datejoined.val());
        var parameters = {
            'action': 'find_scheduling_space',
            'employee': select_employee.val(),
            'date_joined': input_datejoined.val()
        };
        if ($.isEmptyObject(parameters.employee)) {
            alert_sweetalert({
                'title': 'Notificación',
                'type': 'info',
                'message': 'Debe seleccionar un doctor para ver el horario disponible',
                'timer': 2500,
                'callback': function () {

                }
            });
            return false;
        }
        $('.doctor').html('<b>Médico: </b> ' + $('select[name="employee"] option:selected').text());
        tblQuotes = $('#tblQuotes').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: ""
            },
            info: false,
            columns: [
                {data: "hour"},
                {data: "status"},
                {data: "status"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var html = '';
                        switch (row.status) {
                            case 'vacant':
                                html = '<span class="badge badge-success badge-pill">Libre</span>';
                                break;
                            case 'reserved':
                                html = '<span class="badge badge-warning badge-pill">Ocupado</span>';
                                break;
                            case 'time_not_available':
                                html = '<span class="badge badge-danger badge-pill">No disponible</span>';
                                break;
                        }
                        return html;
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.status === 'vacant') {
                            return '<input type="checkbox" class="form-control-checkbox" name="schedule">';
                        }
                        return '---';
                    }
                }
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                if (!$.isEmptyObject(selected_quote)) {
                    if (data.index === selected_quote.index) {
                        tr.find('input[name="schedule"]').prop('checked', 'checked');
                    }
                }
            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
        $('#myModalScheduling').modal('show');
    });

    $('#tblQuotes tbody')
        .off()
        .on('change', 'input[name="schedule"]', function () {
            var tr = tblQuotes.cell($(this).closest('td, li')).index();
            var row = tblQuotes.row(tr.row).data();
            var cells = tblQuotes.cells().nodes();
            $(cells).find('input[type="checkbox"][name="schedule"]').prop('checked', false);
            tblQuotes.rows().data().toArray().forEach(function (value, index, array) {
                value.state = false;
            });
            $(this).prop('checked', true);
            row.state = this.checked;
            row.index = tr.row;
            input_hour.val(row.hour);
            selected_quote = row;
            fv.revalidateField('hour');
        });

    input_hour.val('');
});