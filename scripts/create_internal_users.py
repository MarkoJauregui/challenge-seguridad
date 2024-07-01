from sqlalchemy.orm import Session
from app import models, crud, database
from app.schemas import InternalUserCreate

# Crear una nueva sesión de la base de datos
db: Session = next(database.get_db())

# Verificar si los roles existen antes de crearlos
def get_or_create_role(db: Session, role_name: str, role_description: str):
    role = db.query(models.Role).filter(models.Role.name == role_name).first()
    if not role:
        role = models.Role(name=role_name, description=role_description)
        db.add(role)
        db.commit()
        db.refresh(role)
    return role

# Crear roles si no existen
admin_role = get_or_create_role(db, 'admin', 'Rol de Administrador')
user_role = get_or_create_role(db, 'user', 'Rol de Usuario Regular')

# Crear usuario con rol de administrador si no existe
admin_user = db.query(models.InternalUser).filter(models.InternalUser.username == 'adminuser').first()
if not admin_user:
    admin_user = InternalUserCreate(
        username='adminuser',
        password='adminpassword',
        role_id=admin_role.id  # Asigna el ID del rol de administrador
    )
    crud.create_internal_user(db, admin_user)

# Crear usuario regular si no existe
regular_user = db.query(models.InternalUser).filter(models.InternalUser.username == 'regularuser').first()
if not regular_user:
    regular_user = InternalUserCreate(
        username='regularuser',
        password='regularpassword',
        role_id=user_role.id  # Asigna el ID del rol de usuario regular
    )
    crud.create_internal_user(db, regular_user)

print("Usuarios internos creados exitosamente.")
