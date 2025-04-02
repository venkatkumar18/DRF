1) Activate virtual environment - Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned


Clone repo 
user model - modify settings Auth_user_model
product model (name,desciption,stock,image,price) , in_stock property, str method
Order model (order_id, status, user, created_at) str method, product m2m through, related name, item_subtotal property