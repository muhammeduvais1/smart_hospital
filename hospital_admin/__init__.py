# hospital_admin app
default_app_config = 'hospital_admin.apps.HospitalAdminConfig'
# import signals
try:
	from . import signals  # noqa: F401
except Exception:
	pass
