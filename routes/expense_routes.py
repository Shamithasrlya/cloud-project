from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from db import expenses_collection

expense_bp = Blueprint("expense_bp", __name__)

# Add expense
@expense_bp.route('/add', methods=['POST'])
def add_expense():
    data = request.get_json()

    expense = {
        "user_id": data["user_id"],
        "amount": data["amount"],
        "category": data["category"],
        "description": data["description"],
        "date": data["date"]
    }

    result = expenses_collection.insert_one(expense)
    return jsonify({
        "message": "Expense added successfully",
        "expense_id": str(result.inserted_id) 
    }), 201


# Get all expenses for a user
@expense_bp.route("/<user_id>", methods=["GET"])
def get_expenses(user_id):
    expenses = list(expenses_collection.find({"user_id": user_id}))
    for e in expenses:
        e["_id"] = str(e["_id"])
    return jsonify(expenses), 200

# Delete an expense
@expense_bp.route("/delete/<expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    try:
        result = expenses_collection.delete_one({"_id": ObjectId(expense_id)})
        if result.deleted_count == 1:
            return jsonify({"message": "Expense deleted"}), 200
        else:
            return jsonify({"error": "Expense not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@expense_bp.route('/update/<expense_id>', methods=['PUT'])
def update_expense(expense_id):
    data = request.get_json()

    # Build the update dictionary
    update_data = {}
    if "amount" in data:
        update_data["amount"] = data["amount"]
    if "category" in data:
        update_data["category"] = data["category"]
    if "description" in data:
        update_data["description"] = data["description"]
    if "date" in data:
        update_data["date"] = data["date"]

    result = expenses_collection.update_one(
        {"_id": ObjectId(expense_id)},
        {"$set": update_data}
    )

    if result.modified_count == 1:
        return jsonify({"message": "Expense updated"}), 200
    else:
        return jsonify({"error": "Expense not found or no change"}), 404
