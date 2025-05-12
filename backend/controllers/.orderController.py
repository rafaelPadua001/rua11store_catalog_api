# import sqlite3
# from models.order import Order

# class orderController:
     
#     @staticmethod
#     def get_db_connection():
#         """Cria uma nova conexão com o banco de dados"""
#         conn = sqlite3.connect('database.db', timeout=30.0)  # 10 segundos de timeout
#         conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelos nomes
#         return conn
    
#     def get_order_by_userId(user_id):
#             try:
#                 conn = orderController.get_db_connection()
#                 cursor = conn.cursor()
#                 cursor.execute(""" 
#                     SELECT * FROM orders WHERE user_id = ?
#                 """, (user_id))

#                 order = cursor.fetchall()
#                 conn.close()
#                 if order:
#                     order = Order(
#                         id=order[0]['id'],
#                         user_id=order[0]['user_id'],
#                         payment_id=order[0]['payment_id'],
#                         shipment_info=order[0]['shipment_info'],
#                         order_date=order[0]['order_date'],
#                         total_amount=order[0]['total_amount'],
#                         status=order[0]['status']
#                     )
#                     return order.to_dict()
#                 else:
#                     return None
#             except Exception as e:
#                 raise Exception(f"Erro ao buscar o pedido: {str(e)}")
            
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "user_id": self.user_id,
#             "payment_id": self.payment_id,
#             "shipment_info": self.shipment_info,
#             "order_date": self.order_date,
#             "status": self.status,
#             "total_amount": self.total_amount,
#             "items": self.items  # já é uma lista de dicionários
#         }