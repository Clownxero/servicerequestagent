import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, SYSTEM_PROMPT
from typing import Tuple
import asyncio

async def find_response(query: str) -> Tuple[str, str]:
    try:
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        
        cur = conn.cursor()
        
        # Perform case-insensitive search
        cur.execute("""
            SELECT response, system_prompt 
            FROM responses 
            WHERE LOWER(query) LIKE LOWER(%s)
            LIMIT 1
        """, ('%' + query + '%',))
        
        result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if result:
            return result[0], result[1]
        return "", None  # Return empty response and None for system_prompt
        
    except Exception as e:
        print(f"Database error: {str(e)}")
        return "", None