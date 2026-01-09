# Tarea18 SXE
Manuel Carrera Pazó

## 1º PASO
Una vez tenemos lanzado nuestro contenedor ejecutaremos el siguiente comando para tener la siguiente estructura:
```bash
docker exec -it app_odoo_hospital odoo scaffold Hospital /mnt/extra-addons
```
<img width="273" height="390" alt="image" src="https://github.com/user-attachments/assets/7535e882-f5de-4982-be97-562b4bb37804" />

## 2º PASO
Una vez tenemos esta estructura creada vamos a modificar los siguientes archivos:


### · __manifest__.py
```bash
{
    'name': 'Hospital',
    'version': '1.0.0',
    'category': 'Healthcare',
    'summary': 'Gestión de pacientes y médicos de hospital',
    'description': """
        Módulo para gestionar pacientes, médicos y consultas hospitalarias.
        - Pacientes: nombre, apellidos, síntomas
        - Médicos: nombre, apellidos, número de colegiado
        - Consultas: relación entre paciente y médico con diagnóstico
    """,
    'author': 'Manuel Carrera',
    'website': 'https://www.hospital.com',
    'depends': ['base'],
    'data': [
        'views/views.xml',
    ],
    'installable': True,
    'application': True,
}
```
### · models.py
```bash  
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
```

### · views.py
```bash
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Vista lista de pacientes -->
        <record id="view_paciente_tree" model="ir.ui.view">
            <field name="name">hospital.paciente.tree</field>
            <field name="model">hospital.paciente</field>
            <field name="arch" type="xml">
                <list string="Pacientes">
                    <field name="nombre"/>
                    <field name="apellidos"/>
                    <field name="nombre_completo"/>
                    <field name="sintomas"/>
                </list>
            </field>
        </record>

        <!-- Vista formulario de pacientes -->
        <record id="view_paciente_form" model="ir.ui.view">
            <field name="name">hospital.paciente.form</field>
            <field name="model">hospital.paciente</field>
            <field name="arch" type="xml">
                <form string="Paciente">
                    <sheet>
                        <group>
                            <group>
                                <field name="nombre"/>
                                <field name="apellidos"/>
                                <field name="nombre_completo" readonly="1"/>
                            </group>
                            <group>
                                <field name="sintomas" widget="textarea"/>
                            </group>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>

        <!-- Acción para pacientes -->
        <record id="action_paciente" model="ir.actions.act_window">
            <field name="name">Pacientes</field>
            <field name="res_model">hospital.paciente</field>
            <field name="view_mode">list,form</field>
        </record>

        <!-- Vista lista de médicos -->
        <record id="view_medico_tree" model="ir.ui.view">
            <field name="name">hospital.medico.tree</field>
            <field name="model">hospital.medico</field>
            <field name="arch" type="xml">
                <list string="Médicos">
                    <field name="nombre"/>
                    <field name="apellidos"/>
                    <field name="nombre_completo"/>
                    <field name="numero_colegiado"/>
                </list>
            </field>
        </record>

        <!-- Vista formulario de médicos -->
        <record id="view_medico_form" model="ir.ui.view">
            <field name="name">hospital.medico.form</field>
            <field name="model">hospital.medico</field>
            <field name="arch" type="xml">
                <form string="Médico">
                    <sheet>
                        <group>
                            <field name="nombre"/>
                            <field name="apellidos"/>
                            <field name="nombre_completo" readonly="1"/>
                            <field name="numero_colegiado"/>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>

        <!-- Acción para médicos -->
        <record id="action_medico" model="ir.actions.act_window">
            <field name="name">Médicos</field>
            <field name="res_model">hospital.medico</field>
            <field name="view_mode">list,form</field>
        </record>

        <!-- Vista lista de consultas -->
        <record id="view_consulta_tree" model="ir.ui.view">
            <field name="name">hospital.consulta.tree</field>
            <field name="model">hospital.consulta</field>
            <field name="arch" type="xml">
                <list string="Consultas">
                    <field name="fecha_consulta"/>
                    <field name="paciente_id"/>
                    <field name="medico_id"/>
                    <field name="diagnostico"/>
                </list>
            </field>
        </record>

        <!-- Vista formulario de consultas -->
        <record id="view_consulta_form" model="ir.ui.view">
            <field name="name">hospital.consulta.form</field>
            <field name="model">hospital.consulta</field>
            <field name="arch" type="xml">
                <form string="Consulta">
                    <sheet>
                        <group>
                            <field name="paciente_id"/>
                            <field name="medico_id"/>
                            <field name="fecha_consulta"/>
                        </group>
                        <group>
                            <field name="diagnostico" widget="textarea"/>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>

        <!-- Acción para consultas -->
        <record id="action_consulta" model="ir.actions.act_window">
            <field name="name">Consultas</field>
            <field name="res_model">hospital.consulta</field>
            <field name="view_mode">list,form</field>
        </record>

        <!-- Menús -->
        <menuitem id="menu_hospital" name="Hospital"/>

        <menuitem id="menu_pacientes"
                  name="Pacientes"
                  parent="menu_hospital"
                  action="action_paciente"/>

        <menuitem id="menu_medicos"
                  name="Médicos"
                  parent="menu_hospital"
                  action="action_medico"/>

        <menuitem id="menu_consultas"
                  name="Consultas"
                  parent="menu_hospital"
                  action="action_consulta"/>

</odoo>
```
## COMPROBACIÓNES:
<img width="1299" height="288" alt="image" src="https://github.com/user-attachments/assets/bf562c85-f7cc-415a-b7bb-38361590c8e9" />

### FALLO
Diego, yo diria que lo tengo todo correcto, he probado a cambiar mil cosas pero no me da salido.
Te entrego lo que tengo hecho que me funciona, hasta activar el modulo, luego no me hace nada asique no te puedo poner más comprobaciónes.

