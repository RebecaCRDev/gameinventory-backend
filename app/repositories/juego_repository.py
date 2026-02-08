from typing import Optional, List, Dict, Any
import mysql.connector
from app.core.database import get_connection


SELECT_FIELDS = 'id, codigo, titulo, plataforma, genero, precio, stock, estado, imagen'


def fetch_all(only_activos: bool = True) -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        if only_activos:
            cur.execute(f'''
                SELECT {SELECT_FIELDS}
                FROM juego
                WHERE estado = 1
                ORDER BY id DESC
            ''')
        else:
            cur.execute(f'''
                SELECT {SELECT_FIELDS}
                FROM juego
                ORDER BY id DESC
            ''')
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def fetch_by_id(juego_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(f'''
            SELECT {SELECT_FIELDS}
            FROM juego
            WHERE id = %s
        ''', (juego_id,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def insert(data: Dict[str, Any]) -> int:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO juego (codigo, titulo, plataforma, genero, precio, stock, estado, imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            data.get('codigo'),
            data['titulo'],
            data['plataforma'],
            data.get('genero'),
            data.get('precio', 0.0),
            data.get('stock', 0),
            data.get('estado', 1),
            data.get('imagen')
        ))
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close()
        conn.close()


def update(juego_id: int, data: Dict[str, Any]) -> None:
    conn = get_connection()
    cur = conn.cursor()
    try:
        fields = []
        values = []
        
        if 'codigo' in data:
            fields.append('codigo = %s')
            values.append(data['codigo'])
        if 'titulo' in data:
            fields.append('titulo = %s')
            values.append(data['titulo'])
        if 'plataforma' in data:
            fields.append('plataforma = %s')
            values.append(data['plataforma'])
        if 'genero' in data:
            fields.append('genero = %s')
            values.append(data['genero'])
        if 'precio' in data:
            fields.append('precio = %s')
            values.append(data['precio'])
        if 'stock' in data:
            fields.append('stock = %s')
            values.append(data['stock'])
        if 'estado' in data:
            fields.append('estado = %s')
            values.append(data['estado'])
        if 'imagen' in data:
            fields.append('imagen = %s')
            values.append(data['imagen'])
        
        values.append(juego_id)
        
        query = f"UPDATE juego SET {', '.join(fields)} WHERE id = %s"
        cur.execute(query, tuple(values))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def delete(juego_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM juego WHERE id = %s', (juego_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def toggle_estado(juego_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT estado FROM juego WHERE id = %s', (juego_id,))
        row = cur.fetchone()
        if not row:
            raise KeyError('not_found')
        
        nuevo_estado = 0 if int(row['estado']) == 1 else 1
        cur.execute('UPDATE juego SET estado = %s WHERE id = %s', (nuevo_estado, juego_id))
        conn.commit()
        return nuevo_estado
    finally:
        cur.close()
        conn.close()


def is_duplicate_codigo_error(e: mysql.connector.Error) -> bool:
    msg = str(e)
    return ('Duplicate entry' in msg) and ('codigo' in msg)
