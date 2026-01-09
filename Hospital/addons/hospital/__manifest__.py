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