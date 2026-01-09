from odoo import models, fields, api


class Paciente(models.Model):
    _name = 'hospital.paciente'
    _description = 'Paciente'

    nombre = fields.Char(string='Nombre', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    sintomas = fields.Text(string='Síntomas')

    @api.depends('nombre', 'apellidos')
    def _compute_nombre_completo(self):
        for rec in self:
            rec.nombre_completo = f"{rec.nombre} {rec.apellidos}"

    nombre_completo = fields.Char(
        string='Nombre completo',
        compute='_compute_nombre_completo',
        store=True
    )


class Medico(models.Model):
    _name = 'hospital.medico'
    _description = 'Médico'

    nombre = fields.Char(string='Nombre', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    numero_colegiado = fields.Char(string='Número de Colegiado', required=True)

    @api.depends('nombre', 'apellidos')
    def _compute_nombre_completo(self):
        for rec in self:
            rec.nombre_completo = f"{rec.nombre} {rec.apellidos}"

    nombre_completo = fields.Char(
        string='Nombre completo',
        compute='_compute_nombre_completo',
        store=True
    )


class Consulta(models.Model):
    _name = 'hospital.consulta'
    _description = 'Consulta Médica'

    paciente_id = fields.Many2one(
        'hospital.paciente',
        string='Paciente',
        required=True
    )

    medico_id = fields.Many2one(
        'hospital.medico',
        string='Médico',
        required=True
    )

    diagnostico = fields.Text(string='Diagnóstico', required=True)
    fecha_consulta = fields.Date(string='Fecha de Consulta', default=fields.Date.today)