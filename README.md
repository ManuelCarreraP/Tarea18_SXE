# Tarea18 SXE
Manuel Carrera Pazó

## 1º PASO
Una vez tenemos lanzado nuestro contenedor ejecutaremos el siguiente comando para tener la siguiente estructura:
```bash
docker exec -it odoo18_web_hospital odoo scaffold Hospital /mnt/extra-addons
```
<img width="438" height="518" alt="image" src="https://github.com/user-attachments/assets/14e91c4e-7454-4f4f-ad8f-ef9ff33271bc" />

## 2º PASO
Una vez tenemos esta estructura creada vamos a modificar los siguientes archivos:

### · __manifest__.py
```bash
# -*- coding: utf-8 -*-
{
    'name': "Hospital",

    'summary': "Módulo que permite gestionar pacientes y médicos de un hospital.",

    'description': """
        Para cada paciente, tendremos un modelo con los siguientes datos:
        ● Nombre y apellidos del paciente.
        ● Síntomas.

        Para cada médico, tendremos un modelo con los siguientes datos:
        ● Nombre y apellidos del médico.
        ● Número de colegiado.
        
        Por cada vez que un médico ha atendido a un paciente, tendremos un modelo indicando el diagnóstico.
        Un paciente puede haber sido atendido por varios médicos y un médico puede haber atendido a varios pacientes.
    """,

    'author': "Manuel Carrera",
    'website': "https://www.hospital.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Hospital',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml'
    ],


    'installable': True,
    'application': True,
}

```
### · models.py
```bash  
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HospitalPaciente(models.Model):
    _name = 'hospital.paciente'
    _description = 'Paciente del hospital'

    nombre = fields.Char(
        string='Nombre',
        required=True
    )

    apellidos = fields.Char(
        string='Apellidos',
        required=True
    )

    nombre_completo = fields.Char(
        string='Nombre completo',
        compute='_nombre_completo',
        store=True
    )

    sintomas = fields.Text(
        string='Síntomas'
    )

    consultas_ids = fields.One2many(
        'hospital.consulta',
        'paciente_id',
        string='Consultas realizadas'
    )

    total_consultas = fields.Integer(
        string='Total consultas',
        compute='_calcular_total_consultas',
        store=True
    )

    @api.depends('nombre', 'apellidos')
    def _nombre_completo(self):
        for record in self:
            record.nombre_completo = f"{record.nombre} {record.apellidos}"

    @api.depends('consultas_ids')
    def _calcular_total_consultas(self):
        for record in self:
            record.total_consultas = len(record.consultas_ids)


class HospitalMedico(models.Model):
    _name = 'hospital.medico'
    _description = 'Médico del hospital'

    nombre = fields.Char(
        string='Nombre',
        required=True
    )

    apellidos = fields.Char(
        string='Apellidos',
        required=True
    )

    nombre_completo = fields.Char(
        string='Nombre completo',
        compute='_calcular_nombre_completo',
        store=True
    )

    numero_colegiado = fields.Char(
        string='Número de colegiado',
        required=True
    )

    consultas_ids = fields.One2many(
        'hospital.consulta',
        'medico_id',
        string='Consultas realizadas'
    )

    @api.depends('nombre', 'apellidos')
    def _calcular_nombre_completo(self):
        for record in self:
            record.nombre_completo = f"{record.nombre} {record.apellidos}"


class HospitalConsulta(models.Model):
    _name = 'hospital.consulta'
    _description = 'Consulta médica'

    paciente_id = fields.Many2one(
        'hospital.paciente',
        string='Paciente',
        required=True,
        ondelete='cascade'
    )

    medico_id = fields.Many2one(
        'hospital.medico',
        string='Médico',
        required=True,
        ondelete='restrict'
    )

    diagnostico = fields.Text(
        string='Diagnóstico',
        required=True
    )

    fecha_consulta = fields.Date(
        string='Fecha de consulta',
        default=fields.Date.context_today
    )

    @api.depends('paciente_id.nombre_completo', 'medico_id.nombre_completo', 'fecha_consulta')
    def _calcular_nombre_consulta(self):
        for record in self:
            if record.paciente_id and record.medico_id:
                record.display_name = f"Consulta: {record.paciente_id.nombre_completo} - {record.medico_id.nombre_completo} ({record.fecha_consulta})"
```

```bash
<?xml version="1.0" encoding="utf-8"?>
<odoo>
  <data>

    <!-- Pacientes -->
    <record id="vista_form_paciente" model="ir.ui.view">
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
                            <field name="total_consultas" readonly="1"/>
                        </group>
                        <group>
                            <field name="sintomas" nolabel="1" placeholder="Ej: Dolor de cabeza, fiebre..."/>
                        </group>
                    </group>

                    <notebook>
                        <page string="Historial de consultas">
                            <field name="consultas_ids">
                                <tree>
                                    <field name="fecha_consulta"/>
                                    <field name="medico_id"/>
                                    <field name="diagnostico"/>
                                </tree>
                            </field>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <record id="vista_lista_pacientes" model="ir.ui.view">
        <field name="name">hospital.paciente.tree</field>
        <field name="model">hospital.paciente</field>
        <field name="arch" type="xml">
            <tree string="Pacientes">
                <field name="nombre"/>
                <field name="apellidos"/>
                <field name="nombre_completo"/>
                <field name="total_consultas" decoration-info="total_consultas > 0"/>
                <field name="sintomas"/>
            </tree>
        </field>
    </record>

    <record id="accion_pacientes" model="ir.actions.act_window">
        <field name="name">Pacientes</field>
        <field name="res_model">hospital.paciente</field>
        <field name="view_mode">tree,form</field>
    </record>

    <!-- Médicos -->
    <record id="vista_form_medico" model="ir.ui.view">
        <field name="name">hospital.medico.form</field>
        <field name="model">hospital.medico</field>
        <field name="arch" type="xml">
            <form string="Médico">
                <sheet>
                    <group>
                        <group>
                            <field name="nombre"/>
                            <field name="apellidos"/>
                            <field name="nombre_completo" readonly="1"/>
                            <field name="numero_colegiado"/>
                        </group>
                    </group>

                    <notebook>
                        <page string="Consultas realizadas">
                            <field name="consultas_ids">
                                <tree>
                                    <field name="fecha_consulta"/>
                                    <field name="paciente_id"/>
                                    <field name="diagnostico"/>
                                </tree>
                            </field>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <record id="vista_lista_medicos" model="ir.ui.view">
        <field name="name">hospital.medico.tree</field>
        <field name="model">hospital.medico</field>
        <field name="arch" type="xml">
            <tree string="Médicos">
                <field name="nombre"/>
                <field name="apellidos"/>
                <field name="nombre_completo"/>
                <field name="numero_colegiado"/>
            </tree>
        </field>
    </record>

    <record id="accion_medicos" model="ir.actions.act_window">
        <field name="name">Médicos</field>
        <field name="res_model">hospital.medico</field>
        <field name="view_mode">tree,form</field>
    </record>

    <!-- Consultas -->
    <record id="vista_form_consulta" model="ir.ui.view">
        <field name="name">hospital.consulta.form</field>
        <field name="model">hospital.consulta</field>
        <field name="arch" type="xml">
            <form string="Consulta">
                <sheet>
                    <group>
                        <group>
                            <field name="paciente_id"/>
                            <field name="medico_id"/>
                            <field name="fecha_consulta"/>
                        </group>
                    </group>
                    <field name="diagnostico" nolabel="1" placeholder="Ej: Gripe, descanso 3 días..."/>
                </sheet>
            </form>
        </field>
    </record>

    <record id="vista_lista_consultas" model="ir.ui.view">
        <field name="name">hospital.consulta.tree</field>
        <field name="model">hospital.consulta</field>
        <field name="arch" type="xml">
            <tree string="Consultas">
                <field name="fecha_consulta"/>
                <field name="paciente_id"/>
                <field name="medico_id"/>
                <field name="diagnostico"/>
            </tree>
        </field>
    </record>

    <record id="accion_consultas" model="ir.actions.act_window">
        <field name="name">Consultas</field>
        <field name="res_model">hospital.consulta</field>
        <field name="view_mode">tree,form</field>
    </record>

    <!-- Menú -->
    <menuitem id="menu_hospital" name="Hospital"/>

    <menuitem id="menu_pacientes" name="Pacientes" parent="menu_hospital" action="accion_pacientes"/>
    <menuitem id="menu_medicos" name="Médicos" parent="menu_hospital" action="accion_medicos"/>
    <menuitem id="menu_consultas" name="Consultas" parent="menu_hospital" action="accion_consultas"/>

  </data>
</odoo>
```

```bash
services:
  db:
    image: postgres:17
    container_name: odoo18_db_hospital
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=odoo
      - POSTGRES_PASSWORD=odoo
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  web:
    image: odoo:18.0
    container_name: odoo18_web_hospital
    depends_on:
      - db
    ports:
      - "8069:8069"
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo
    volumes:
      - web_data:/var/lib/odoo
      - ./config:/etc/odoo
      - ./addons:/mnt/extra-addons

    restart: unless-stopped

  pgadmin:
    image: dpage/pgadmin4
    container_name: pgadmin_odoo18_hospital
    depends_on:
      - db
    ports:
      - "8080:80"
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@gmail.com
      - PGADMIN_DEFAULT_PASSWORD=admin
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    restart: unless-stopped

volumes:
  postgres_data:
  web_data:
  pgadmin_data:

 # vsas-kvvu-8wwh
```
