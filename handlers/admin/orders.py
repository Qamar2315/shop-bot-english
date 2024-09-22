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
        order_id = order[3]
        user_name = order[1]
        user_address = order[2]
        products = order[3] 

        product_list = []
        for item in products.split(' '):
            idx, quantity = item.split('=')
            product_data = db.fetchone('SELECT title, price FROM products WHERE idx=?', (idx,)) 
            if product_data:
                product_title, product_price = product_data
                product_list.append(f'  * {product_title} ({quantity} pcs, {product_price}£)') 
            else:
                product_list.append(f'  * Product not found (ID: {idx})')

        # Improved formatting:
        res += f"**Order №{order_id}**\n"
        res += f"**User:** {user_name}\n"
        res += f"**Address:** {user_address}\n"
        res += f"**Products:**\n"
        res += '\n'.join(product_list)

    await message.answer(res)