from typing import Optional, List, Dict, Any
from app.core.database import get_connection


def fetch_all() -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute('''
            SELECT id, nombre, email, rol, estado, fecha_creacion
            FROM usuario
            ORDER BY id DESC
        ''')
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def fetch_by_id(usuario_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute('''
            SELECT id, nombre, email, rol, estado, fecha_creacion
            FROM usuario
            WHERE id = %s
        ''', (usuario_id,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def fetch_by_email(email: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute('''
            SELECT id, nombre, email, password, rol, estado, fecha_creacion
            FROM usuario
            WHERE email = %s
        ''', (email,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def insert(data: Dict[str, Any]) -> int:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO usuario (nombre, email, password, rol, estado)
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            data['nombre'],
            data['email'],
            data['password'],
            data.get('rol', 'usuario'),
            data.get('estado', 1)
        ))
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close()
        conn.close()


def update(usuario_id: int, data: Dict[str, Any]) -> None:
    conn = get_connection()
    cur = conn.cursor()
    try:
        fields = []
        values = []
        
        if 'nombre' in data:
            fields.append('nombre = %s')
            values.append(data['nombre'])
        if 'email' in data:
            fields.append('email = %s')
            values.append(data['email'])
        if 'password' in data:
            fields.append('password = %s')
            values.append(data['password'])
        if 'rol' in data:
            fields.append('rol = %s')
            values.append(data['rol'])
        if 'estado' in data:
            fields.append('estado = %s')
            values.append(data['estado'])
        
        values.append(usuario_id)
        
        query = f"UPDATE usuario SET {', '.join(fields)} WHERE id = %s"
        cur.execute(query, tuple(values))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def delete(usuario_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM usuario WHERE id = %s', (usuario_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()
