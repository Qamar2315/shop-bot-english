from aiogram.types import Message
from loader import dp, db
from handlers.user.menu import orders
from filters import IsAdmin

@dp.message_handler(IsAdmin(), text=orders)
async def process_orders(message: Message):
    
    orders = db.fetchall('SELECT * FROM orders')
    
    if len(orders) == 0: 
        await message.answer('You have no orders.')
    else: 
        await order_answer(message, orders)

# async def order_answer(message, orders):

#     res = ''

#     for order in orders:
#         res += f'Order <b>№{order[3]}</b>\n\n'

#     await message.answer(res)

async def order_answer(message, orders):

    res = ''

    for order in orders:
        # Assuming your 'orders' table has these columns:
        # cid, usr_name, usr_address, products, status 
        # ... You can adjust the column names if they are different.

        order_id = order[3]  # Assuming order ID is in the 4th column
        user_name = order[1]
        user_address = order[2]
        products = order[3]  # Assuming products are stored as a string (e.g., 'idx1=quantity1 idx2=quantity2')
        # status = 'Paid' if order[4] == 1 else 'Pending'

        # Parse the products string into a readable list
        product_list = []
        for item in products.split(' '):
            idx, quantity = item.split('=')
            product_data = db.fetchone('SELECT title, price FROM products WHERE idx=?', (idx,)) 
            if product_data:
                product_title, product_price = product_data
                product_list.append(f'  * {product_title} ({quantity} pcs, {product_price}£)') 
            else:
                product_list.append(f'  * Product not found (ID: {idx})')

        # Construct the formatted order details
        res += f'Order <b>№{order_id}</b>\n'
        res += f'User: {user_name}\n'
        res += f'Address: {user_address}\n'
        res += f'Products:\n'
        res += '\n'.join(product_list)
        # res += f'Status: {status}\n\n'

    await message.answer(res)