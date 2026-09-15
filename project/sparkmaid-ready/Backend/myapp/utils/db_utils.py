import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from datetime import datetime, timedelta

#establish connection
def get_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("Database connection established successfully.")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# create customer table
def create_customer_table():
    query = """
    CREATE TABLE IF NOT EXISTS customer (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone_number VARCHAR(15) NOT NULL UNIQUE,
        address TEXT,
        email VARCHAR(100) UNIQUE,
        gender ENUM('Male','Female','Other'),
        dob DATE,
        age INT,
        otp VARCHAR(10),
        otp_expiry DATETIME,
        service_registered VARCHAR(100),
        username VARCHAR(50) UNIQUE,
        password VARCHAR(255) NOT NULL,
        status ENUM('PENDING','ACTIVE','INACTIVE') DEFAULT 'PENDING',
        created_by VARCHAR(50),
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_by VARCHAR(50),
        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        deleted_by VARCHAR(50),
        deleted_date DATETIME DEFAULT NULL
    )
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            print("Customer table created successfully.")
        except Error as e:
            print(f"Error while creating customer table: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to database.")

#creating new customer
def insert_customer(name, phone_number, address, email, gender, dob, age,
                    username, password, otp, created_by, service_registered):
    
    conn = get_connection()
    if not conn:
        return False, "Database connection failed"

    try:
        cursor = conn.cursor()
        conn.start_transaction()
        cursor.execute("SELECT username FROM customer WHERE  phone_number=%s OR username=%s",
                       ( phone_number, username))
        if cursor.fetchone():
            conn.rollback()
        otp_expiry = datetime.now() + timedelta(minutes=10)

        query = """
        INSERT INTO customer (
            name, phone_number, address, email, gender, dob, age,
            username, password, service_registered, otp, otp_expiry, status, created_by
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'PENDING', %s)
        """

        cursor.execute(query, (
            name, phone_number, address, email, gender, dob, age, 
            username, password, service_registered, otp, otp_expiry, created_by
        ))
        conn.commit()
        print(f"Customer inserted successfully")
        return True, None
    except Exception as e:
        conn.rollback()
        print(f" Error inserting customer: {e}")
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


# retrive customer email
def get_customer_by_email(email):
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customer WHERE email=%s", (email,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def get_admin_by_email(email):
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE email=%s", (email,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

# activate customer by otp
def activate_customer(email):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE customer SET status='ACTIVE', otp=NULL WHERE email=%s", (email,))
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()

# Update OTP with expiry (used for registration & forgot password)
def update_customer_otp(email, otp):
    
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        otp_expiry = datetime.now() + timedelta(minutes=5)
        cursor.execute("UPDATE customer SET otp=%s, otp_expiry=%s WHERE email=%s", (otp, otp_expiry, email))
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()

#   """Update customer password"""
def update_customer_password(email, new_password):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE customer SET password=%s WHERE email=%s", (new_password, email))
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()

def update_admin_password(email, new_password):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE admin SET password=%s WHERE email=%s", (new_password, email))
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()

# """Fetch all active (non-deleted) customers"""
def get_all_customers():
    conn = get_connection()
    if not conn:
        return None, "Database connection failed"

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT customer_id, name, phone_number, address, email, gender, dob, age,
             service_registered, username, status, created_by, created_date,
               updated_by, updated_date
        FROM customer
        WHERE status != 'DELETED'
        ORDER BY created_date DESC
        """
        cursor.execute(query)
        customers = cursor.fetchall()
        return customers, None
    except Exception as e:
        return None, str(e)
    finally:
        cursor.close()
        conn.close()

#   """Fetch a single customer by ID"""
def get_customer_by_id(customer_id):
    conn = get_connection()
    if not conn:
        return None, "Database connection failed"
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT customer_id, name, phone_number, address, email, gender, dob, age,
              service_registered, username, status, created_by, created_date,
               updated_by, updated_date
        FROM customer
        WHERE customer_id = %s AND status != 'DELETED'
        """
        cursor.execute(query, (customer_id,))
        customer = cursor.fetchone()
        return customer, None
    except Exception as e:
        return None, str(e)
    finally:
        cursor.close()
        conn.close()

# update customer details
def update_customer(customer_id, update_data):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customer WHERE customer_id = %s AND deleted_by IS NULL", (customer_id,))
        existing_customer = cursor.fetchone()

        if not existing_customer:
            cursor.close()
            conn.close()
            return None, "Customer not found"
        fields_to_update = []
        values = []

        for key, value in update_data.items():
            if key in existing_customer and existing_customer[key] != value:
                fields_to_update.append(f"{key} = %s")
                values.append(value)
        if not fields_to_update:
            cursor.close()
            conn.close()
            return None, "No changes made"

        fields_to_update.append("updated_date = CURRENT_TIMESTAMP")
        fields_to_update.append("updated_by = %s")
        values.append(update_data.get("updated_by", "system"))

        query = f"UPDATE customer SET {', '.join(fields_to_update)} WHERE customer_id = %s"
        values.append(customer_id)

        cursor.execute(query, tuple(values))
        conn.commit()

        cursor.close()
        conn.close()
        return True, None
    except Exception as e:
        return None, str(e)

# soft delete customer details
def soft_delete_customer(customer_id, deleted_by):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customer WHERE customer_id = %s AND deleted_by IS NULL", (customer_id,))
        existing = cursor.fetchone()

        if not existing:
            cursor.close()
            conn.close()
            return None, "Customer not found or already deleted"
        query = """
            UPDATE customer
            SET status = 'INACTIVE',
                deleted_by = %s,
                deleted_date = CURRENT_TIMESTAMP
            WHERE customer_id = %s
        """
        cursor.execute(query, (deleted_by, customer_id))
        conn.commit()

        cursor.close()
        conn.close()
        return True, None
    except Exception as e:
        return None, str(e)

 # ------------------------------------------------- MAID ------------------------------------------------------------------------------- #

# create maid table
def create_maid_table():
    query = """
    CREATE TABLE IF NOT EXISTS maid (
        maid_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone_number VARCHAR(15) NOT NULL UNIQUE,
        address TEXT,
        email VARCHAR(100) UNIQUE,
        gender ENUM('Male', 'Female', 'Other'),
        dob DATE,
        age INT,
        experience_years INT,
        service VARCHAR(100),                 
        salary DECIMAL(10,2),                 
        availability_status ENUM('AVAILABLE', 'BOOKED', 'INACTIVE') DEFAULT 'AVAILABLE',
        created_by VARCHAR(50),
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_by VARCHAR(50),
        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        deleted_by VARCHAR(50),
        deleted_date DATETIME DEFAULT NULL
    )
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            print(" Maid table created successfully.")
        except Error as e:
            print(f" Error while creating maid table: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to database.")

# insert new maid
def insert_maid(name, phone_number, address, email, gender, dob, age, 
                experience_years, service, salary, created_by):
    conn = get_connection()
    if not conn:
        return False, "Database connection failed"
    try:
        cursor = conn.cursor()
        conn.start_transaction()
        cursor.execute("""
            SELECT maid_id FROM maid 
            WHERE email=%s OR phone_number=%s 
        """, (email, phone_number,))
        if cursor.fetchone():
            conn.rollback()
            return False, "Maid with same email, phone number, or already exists"
        query = """
        INSERT INTO maid
        (name, phone_number, address, email, gender, dob, age, 
         experience_years, service, salary, availability_status, created_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'AVAILABLE', %s)
        """
        cursor.execute(query, (
            name, phone_number, address, email, gender, dob, age, 
            experience_years, service, salary, created_by
        ))
        conn.commit()
        print("Maid record inserted successfully.")
        return True, None
    except Exception as e:
        print(f"Error inserting maid: {e}")
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

# retrive maid by id
def get_maid_by_id(maid_id):
    conn = get_connection()
    if not conn:
        return None, "Database connection failed"
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT maid_id, name, phone_number, address, email, gender, 
               dob, age, experience_years, service, 
               salary, availability_status, created_by, created_date, 
               updated_by, updated_date
        FROM maid 
        WHERE maid_id = %s AND deleted_date IS NULL
        """
        cursor.execute(query, (maid_id,))
        maid = cursor.fetchone()
        if maid:
            if maid.get('dob'):
                maid['dob'] = maid['dob'].strftime('%Y-%m-%d')
            if maid.get('created_date'):
                maid['created_date'] = maid['created_date'].strftime('%Y-%m-%d %H:%M:%S')
            if maid.get('updated_date'):
                maid['updated_date'] = maid['updated_date'].strftime('%Y-%m-%d %H:%M:%S')
            return maid, None
        else:
            return None, "Maid not found"
    except Error as e:
        return None, f"Database error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# """Get all maids with optional filters"""
def get_all_maids(filters=None):
    conn = get_connection()
    if not conn:
        return None, "Database connection failed"
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT maid_id, name, phone_number, address, email, gender, 
               dob, age, experience_years, service, 
               salary, availability_status, created_by, created_date
        FROM maid 
        WHERE deleted_date IS NULL
        """
        params = []
        if filters:
            if filters.get('availability_status'):
                query += " AND availability_status = %s"
                params.append(filters['availability_status'])
            
            if filters.get('gender'):
                query += " AND gender = %s"
                params.append(filters['gender'])
            
            if filters.get('service'):
                query += " AND service LIKE %s"
                params.append(f"%{filters['service']}%")
        
        query += " ORDER BY created_date DESC"
        cursor.execute(query, params)
        maids = cursor.fetchall()
        for maid in maids:
            if maid.get('dob'):
                maid['dob'] = maid['dob'].strftime('%Y-%m-%d')
            if maid.get('created_date'):
                maid['created_date'] = maid['created_date'].strftime('%Y-%m-%d %H:%M:%S')
        
        return maids, None
    except Error as e:
        return None, f"Database error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# update maid details
def update_maid(maid_id, update_data):
    conn = get_connection()
    if not conn:
        return False, "Database connection failed"
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT maid_id FROM maid WHERE maid_id = %s AND deleted_date IS NULL", (maid_id,))
        if not cursor.fetchone():
            return False, "Maid not found"
        update_fields = []
        params = []
        allowed_fields = [
            'name', 'phone_number', 'address', 'email', 'gender', 
            'dob', 'age',  'experience_years', 
            'service', 'salary', 'availability_status','status' ,'updated_by'
        ]
        
        for field in allowed_fields:
            if field in update_data and update_data[field] is not None:
                update_fields.append(f"{field} = %s")
                params.append(update_data[field])
        if not update_fields:
            return False, "No fields to update"
        params.append(maid_id)
        query = f"""
        UPDATE maid 
        SET {', '.join(update_fields)}
        WHERE maid_id = %s AND deleted_date IS NULL
        """
        cursor.execute(query, params)
        conn.commit()
        if cursor.rowcount == 0:
            return False, "No changes made" 
        print(f" Maid ID updated successfully")
        return True, None
    except Error as e:
        error_msg = str(e)
        if "Duplicate entry" in error_msg:
            if "phone_number" in error_msg:
                return False, "Phone number already exists"
            elif "email" in error_msg:
                return False, "Email already exists"
        return False, f"Database error: {error_msg}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# soft delete maid
def delete_maid(maid_id, deleted_by):
    conn = get_connection()
    if not conn:
        return False, "Database connection failed"
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT maid_id FROM maid WHERE maid_id = %s AND deleted_date IS NULL", (maid_id,))
        if not cursor.fetchone():
            return False, "Maid not found or already deleted"
        
        query = """
            UPDATE maid
            SET deleted_date = %s,
                deleted_by = %s,
                availability_status = 'INACTIVE'
            WHERE maid_id = %s AND deleted_date IS NULL
        """
        cursor.execute(query, (datetime.now(), deleted_by, maid_id))
        conn.commit()

        if cursor.rowcount == 0:
            return False, "No rows updated (maid may already be deleted)"
        print(f" Maid IDd eleted by {deleted_by}")
        return True, None

    except Error as e:
        return False, f"Database error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# -------------------admin--------------------------
# create admin table
def create_admin_table():
    query = """
    CREATE TABLE IF NOT EXISTS admin (
        admin_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone_number VARCHAR(15) UNIQUE,
        address TEXT,
        email VARCHAR(100) UNIQUE NOT NULL,
        gender ENUM('Male','Female','Other'),
        dob DATE,
        age INT,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_by VARCHAR(50),
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_by VARCHAR(50),
        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        deleted_by VARCHAR(50),
        deleted_date TIMESTAMP NULL
    )
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            print("Admin table created successfully.")
        except Exception as e:
            print(f"Error creating admin table: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to database.")

# insert admin
def insert_admin(name, phone_number, address, email, gender, dob, age,  username, password, created_by):
    conn = get_connection()
    if not conn:
        return False, "Database connection failed"
    try:
        cursor = conn.cursor()
        conn.start_transaction()  
        cursor.execute("""
            SELECT admin_id FROM admin 
            WHERE email=%s OR username=%s 
        """, (email, username))
        if cursor.fetchone():
            conn.rollback()
            return False, "Admin with same email, username, or  already exists"
        query = """
        INSERT INTO admin
        (name, phone_number, address, email, gender, dob, age, username, password, created_by)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(query, (name, phone_number, address, email, gender, dob, age,  username, password,created_by))
        conn.commit()
        return True, None
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

# retrive admin details
def get_all_admins():
    conn = get_connection()
    if not conn:
        return None, "Database connection failed"
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE deleted_date IS NULL")
        admins = cursor.fetchall()
        return admins, None
    except Exception as e:
        return None, str(e)
    finally:
        cursor.close()
        conn.close()

#update admin details
def update_admin_details(admin_id, update_data):
    conn = get_connection()
    if not conn:
        return None, "Database connection failed"

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE admin_id = %s AND deleted_date IS NULL", (admin_id,))
        existing_admin = cursor.fetchone()
        if not existing_admin:
            return None, "Admin not found"
        updates = []
        values = []
        for key, value in update_data.items():
            if key in existing_admin and str(existing_admin[key]) != str(value):
                updates.append(f"{key} = %s")
                values.append(value)

        if not updates:
            return "no_change", None 

        update_query = f"UPDATE admin SET {', '.join(updates)}, updated_date = NOW(), updated_by = %s WHERE admin_id = %s"
        values.append(update_data.get("updated_by", "system"))
        values.append(admin_id)

        cursor.execute(update_query, tuple(values))
        conn.commit()

        return "success", None
    except Exception as e:
        return None, str(e)
    finally:
        cursor.close()
        conn.close()
    


# ------booking history_____________________________
# stores the booking details
def create_booking_table():
    query = """
    CREATE TABLE IF NOT EXISTS booking (
        booking_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT NOT NULL,
        maid_id INT NOT NULL,
        service VARCHAR(100) NOT NULL,
        booking_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        status ENUM('PENDING','CONFIRMED','CANCELLED','COMPLETED') DEFAULT 'PENDING',
        payment DECIMAL(10,2) DEFAULT 0.00,
        duration INT DEFAULT 0,
        payment_date DATETIME DEFAULT NULL,
        created_by VARCHAR(50),
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_by VARCHAR(50),
        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
        FOREIGN KEY (maid_id) REFERENCES maid(maid_id)
    )
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            print("Booking table created successfully.")
        except Error as e:
            print(f"Error creating booking table: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to database.")


# create booking history
def insert_booking(customer_id, maid_id, service, duration=0, payment=0.0, created_by="system"):
    conn = get_connection()
    if not conn:
        return False, "Database connection failed"
    
    try:
        cursor = conn.cursor()
        conn.start_transaction()  
        
        # Check customer exists
        cursor.execute("SELECT customer_id FROM customer WHERE customer_id=%s AND deleted_date IS NULL", (customer_id,))
        if not cursor.fetchone():
            conn.rollback()
            return False, "Customer not found"
        
        # Check maid exists and is available
        cursor.execute("SELECT maid_id FROM maid WHERE maid_id=%s AND deleted_date IS NULL AND availability_status='AVAILABLE'", (maid_id,))
        if not cursor.fetchone():
            conn.rollback()
            return False, "Maid not found or not available"
        
        # Insert booking
        query = """
        INSERT INTO booking (customer_id, maid_id, service, duration, payment, created_by)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (customer_id, maid_id, service, duration, payment, created_by))
        conn.commit()
        return True, None
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


# retrive by customer id
def get_booking_history_by_customer(customer_id):
    conn = get_connection()
    if not conn:
        return None, "Database connection failed"
    try:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT name, status FROM customer WHERE customer_id=%s AND deleted_date IS NULL",
            (customer_id,)
        )
        customer = cursor.fetchone()
        if not customer:
            return None, "Customer not found"
        if customer["status"] != "ACTIVE":
            return None, "Customer is inactive"
        query = """
        SELECT 
            b.booking_id, b.service, b.booking_date, b.status,
            m.name AS maid_name, m.phone_number AS maid_phone
        FROM booking b
        JOIN maid m ON b.maid_id = m.maid_id
        WHERE b.customer_id=%s
        ORDER BY b.booking_date DESC
        """
        cursor.execute(query, (customer_id,))
        bookings = cursor.fetchall()

        if not bookings:
            return None, "No bookings found for this customer"

        return bookings, None

    except Error as e:
        return None, str(e)
    finally:
        cursor.close()
        conn.close()


# get all history for admin
def get_all_booking_history():
    conn = get_connection()
    if not conn:
        return None, "Database connection failed"
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT b.booking_id, b.service, b.booking_date, b.status,
               m.name AS maid_name, m.phone_number AS maid_phone,
               c.name AS customer_name, c.phone_number AS customer_phone,b.payment,b.payment_date,b.duration
        FROM booking b
        JOIN customer c ON b.customer_id = c.customer_id
        JOIN maid m ON b.maid_id = m.maid_id
        ORDER BY b.booking_date 
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return result, None
    except Error as e:
        return None, str(e)
    finally:
        cursor.close()
        conn.close()

# update booking details
def update_booking(booking_id, update_data):
   
    conn = get_connection()
    if not conn:
        return False, "Database connection failed"
    
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM booking WHERE booking_id=%s AND status != 'CANCELLED'", (booking_id,))
        booking = cursor.fetchone()
        if not booking:
            return False, "Booking not found or already cancelled"
        
        allowed_fields = ['service', 'status', 'maid_id', 'payment', 'duration', 'payment_date', 'updated_by']
        set_clauses = []
        params = []
        
        for field in allowed_fields:
            if field in update_data and update_data[field] is not None:
                if field == 'payment_date' and update_data[field] == 'CURRENT_TIMESTAMP':
                    set_clauses.append(f"{field} = CURRENT_TIMESTAMP")
                else:
                    set_clauses.append(f"{field} = %s")
                    params.append(update_data[field])
        
        if not set_clauses:
            return False, "No fields to update"
     
        params.append(booking_id)
        
        query = f"UPDATE booking SET {', '.join(set_clauses)}, updated_date = CURRENT_TIMESTAMP WHERE booking_id = %s"
        cursor.execute(query, params)
        conn.commit()
        
        if cursor.rowcount == 0:
            return False, "No changes made"
        
        return True, None

    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


# retrive by customer id
def get_booking_history(booking_id):
    conn = get_connection()
    if not conn:
        return None, "Database connection failed"

    try:
        cursor = conn.cursor(dictionary=True)

        # Fetch booking with customer & maid info
        query = """
        SELECT 
            b.booking_id,
            b.customer_id,
            c.name AS customer_name,
            c.status AS customer_status,
            m.name AS maid_name,
            m.phone_number AS maid_phone,
            b.service,
            b.duration,
            b.payment,
            b.payment_date,
            b.status AS booking_status,
            b.booking_date
        FROM booking b
        JOIN customer c ON b.customer_id = c.customer_id
        JOIN maid m ON b.maid_id = m.maid_id
        WHERE b.booking_id = %s
        """
        cursor.execute(query, (booking_id,))
        booking = cursor.fetchone()

        if not booking:
            return None, "Booking not found"

        # Optionally ensure customer is active
        if booking["customer_status"] != "ACTIVE":
            return None, "Customer is inactive"

        return booking, None

    except Error as e:
        return None, str(e)

    finally:
        cursor.close()
        conn.close()
