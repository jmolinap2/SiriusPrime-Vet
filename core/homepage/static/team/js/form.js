var tblSocialNetworks;
var team = {
    social_networks: [],
    add: function (item) {
        this.social_networks.push(item);
        this.list();
    },
    list: function () {
        tblSocialNetworks = $('#tblSocialNetworks').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.social_networks,
            columns: [
                {data: "name"},
                {data: "name"},
                {data: "icon"},
                {data: "url"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fas fa-times"></i></a>';
                    }
                },
                {
                    targets: [1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control form-control-sm" placeholder="Ingrese un mombre" autocomplete="off" name="name" value="' + row.name + '">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control form-control-sm" placeholder="Ingrese un icono" autocomplete="off" name="icon" value="' + row.icon + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control form-control-sm" placeholder="Ingrese una dirección url" autocomplete="off" name="url" value="' + row.url + '">';
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
};

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
            },
            fields: {
                names: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                job: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                description: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                phrase: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                image: {
                    validators: {
                        file: {
                            extension: 'jpeg,jpg,png',
                            type: 'image/jpeg,image/png',
                            maxFiles: 1,
                            message: 'Introduce una imagen válida'
                        }
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
            if (team.social_networks.length === 0) {
                message_error('Debe tener al menos un item en el detalle');
                return false;
            }
            var params = new FormData(fv.form);
            params.append('social_networks', JSON.stringify(team.social_networks));
            var args = {
                'params': params,
                'form': fv.form
            };
            submit_with_formdata(args);
        });
});

$(function () {

    $('.btnRemoveAll').on('click', function () {
        if (team.social_networks.length === 0) return false;
        dialog_action({
            'content': '¿Estas seguro de eliminar todos los items de tu detalle?',
            'success': function () {
                team.social_networks = [];
                team.list();
            },
            'cancel': function () {

            }
        });
    });

    $('.btnAdd').on('click', function () {
        team.add({
            'name': '',
            'icon': '',
            'url': '',
        });
    });

    $('#tblSocialNetworks tbody')
        .off()
        .on('keyup', 'input[name="name"]', function () {
            var tr = tblSocialNetworks.cell($(this).closest('td, li')).index();
            team.social_networks[tr.row].name = $(this).val();
        })
        .on('keyup', 'input[name="url"]', function () {
            var tr = tblSocialNetworks.cell($(this).closest('td, li')).index();
            team.social_networks[tr.row].url = $(this).val();
        })
        .on('keyup', 'input[name="icon"]', function () {
            var tr = tblSocialNetworks.cell($(this).closest('td, li')).index();
            team.social_networks[tr.row].icon = $(this).val();
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblSocialNetworks.cell($(this).closest('td, li')).index();
            team.social_networks.splice(tr.row, 1);
            tblSocialNetworks.row(tr.row).remove().draw();
        });
});