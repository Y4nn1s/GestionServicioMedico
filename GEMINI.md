# Sistema de Gestión Médica UNEARTE

## Project Overview

This is a comprehensive medical management system built with Django for UNEARTE (Universidad Experimental "Rafael María Baralt"). It's designed to manage patients, appointments, medical records, and inventory for a healthcare facility. The system includes modules for patient management, appointment scheduling, medical history tracking, and pharmaceutical inventory control.

### Main Technologies
- **Framework**: Django 5.2.6
- **Database**: PostgreSQL (using psycopg2)
- **Frontend**: Bootstrap 5.3 with Bootstrap Icons
- **Template Engine**: Django's built-in template system
- **Language**: Python 3.13.3

### Architecture

The system is organized into several Django applications:

#### Core App
- Dashboard with statistics and quick access
- Authentication and authorization
- Main navigation and layout

#### Pacientes App
- Patient management with personal information
- Address and phone number tracking
- Geographic hierarchy (Country → State → City)
- Gender options (Masculine/Feminine)
- Document type management (focus on Venezuelan ID)

#### Citas App
- Appointment scheduling system
- Multiple appointment types and reasons
- Status tracking (pending, completed, canceled, etc.)
- Time-based scheduling with start/end times
- Notes system for appointments

#### Historiales App
- Medical history tracking
- Allergies and pre-existing conditions
- Current medications
- Patient-specific health records

#### Inventario App
- Pharmaceutical inventory management
- Medicine catalog with auto-generated codes
- Stock tracking and minimum stock levels
- Supplier management
- Category organization
- Expiration date tracking
- Inventory movement tracking

## Building and Running

### Prerequisites
- Python 3.13+
- PostgreSQL server
- Virtual environment (recommended)

### Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL database:
   - Create a database named `sistema_unearte`
   - Update database credentials in environment variables if needed

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Environment Variables

The system uses environment variables for configuration (with defaults):
- `DB_NAME` - Database name (default: 'sistema_unearte')
- `DB_USER` - Database user (default: 'postgres')
- `DB_PASSWORD` - Database password (default: 'postgres')
- `DB_HOST` - Database host (default: 'localhost')
- `DB_PORT` - Database port (default: '5432')

## Development Conventions

### Code Style
- Follows standard Django project structure
- Model names are in singular form
- Uses Django's built-in form handling
- Template inheritance with base.html

### Naming Conventions
- Database table names use custom prefixes (e.g., 'inventario_medicamentos')
- Foreign key relationships use descriptive names
- URL patterns use namespace organization

### Data Validation
- Client and server-side validation
- Unique constraints where appropriate
- Required field validation
- Foreign key integrity

### Security
- CSRF protection
- Input sanitization
- Authentication for protected views
- Session management
