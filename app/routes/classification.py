from app.routes import bp
from flask import render_template, session, redirect, url_for, request, flash, jsonify
import secrets
from app import mongo
from bson import ObjectId
from bson.json_util import dumps



@bp.route('/api/tickets', methods=['GET'])
def get_tickets():
    collection_name = "issues"  # Specify your collection name here
    tickets = mongo.db[collection_name].find()
    return dumps(tickets)


# View class details route with class_id: Render class details page

@bp.route('/class/<class_id>', methods=['GET', 'POST'])
def class_details(class_id):
    class_data = mongo.db.classes.find_one({'_id': ObjectId(class_id)})
    examples = list(mongo.db.examples.find({'class_id': ObjectId(class_id)}))
    
    return render_template('class_details.html', class_details=class_data, examples=examples, class_id=class_id)

# Add class credentials POST request route: Handle adding new class credentials
@bp.route('/new_class_credentials', methods=['POST'])
def new_class_credentials():
    name = request.form.get('name')
    description = request.form.get('description')
    examples = request.form.getlist('examples[]')
    autoresponses = request.form.getlist('autoresponses[]')

    class_id = secrets.randbelow(1000)  # Generate a random class_id

    # Insert class details into 'add_class' collection in MongoDB
    mongo.db.add_class.insert_one({
        'class_id': class_id,
        'class_name': name,
        'description': description
    })

    # Insert examples into 'examples' collection
    for example in examples:
        mongo.db.examples.insert_one({
            'class_id': class_id,
            'example_data': example
        })

    # Insert autoresponses into 'autoresponses' collection
    for autoresponse in autoresponses:
        if autoresponse:  # Only insert non-empty autoresponses
            mongo.db.autoresponses.insert_one({
                'class_id': class_id,
                'response': autoresponse
            })

    flash('Class added successfully with examples and autoresponses', 'success')
    return redirect(url_for('auth.classification_config'))

# Add class page route: Render add class page
@bp.route('/add_class')
def add_class():
    return render_template('add_class.html')

# Delete class route with class_id: Handle deleting class
@bp.route('/delete_class/<class_id>', methods=['DELETE'])
def delete_class(class_id):
    try:
        result = mongo.db.add_class.delete_one({'class_id': int(class_id)})
        if result.deleted_count == 1:
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'error': 'Class not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    


@bp.route('/view_class_details/<class_id>')
def view_class_details(class_id):
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    try:
        class_details = mongo.db.add_class.find_one({'class_id': int(class_id)})
        if not class_details:
            flash('Class not found', 'danger')
            return render_template('view_class_details.html', class_details=None, examples=None, autoresponses=None)

        examples = list(mongo.db.examples.find({'class_id': int(class_id)}))
        autoresponses = list(mongo.db.autoresponses.find({'class_id': int(class_id)}))
        return render_template('view_class_details.html', class_details=class_details, examples=examples, autoresponses=autoresponses)
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return render_template('view_class_details.html', class_details=None, examples=None, autoresponses=None)




@bp.route('/add_example/<int:class_id>', methods=['POST'])
def add_example(class_id):
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'User not logged in'}), 401

    example_data = request.form.get('example_data')

    if not example_data:
        return jsonify({'success': False, 'error': 'Example is required'}), 400

    try:
        mongo.db.examples.insert_one({
            'class_id': class_id,
            'example_data': example_data,
        })
        return jsonify({'success': True, 'message': 'Example added successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    

@bp.route('/add_autoresponse/<int:class_id>', methods=['POST'])
def add_autoresponse(class_id):
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'User not logged in'}), 401

    autoresponse_data = request.form.get('autoresponse_data')

    if not autoresponse_data:
        return jsonify({'success': False, 'error': 'Autoresponse is required'}), 400

    try:
        mongo.db.autoresponses.insert_one({
            'class_id': class_id,
            'response': autoresponse_data,
        })
        return jsonify({'success': True, 'message': 'Autoresponse added successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    


@bp.route('/edit_example/<class_id>/<example_id>', methods=['POST'])

def edit_example(class_id, example_id):
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'User not logged in'}), 401

    data = request.json
    new_example_data = data.get('data')

    if not new_example_data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    try:
        result = mongo.db.examples.update_one(
            {'_id': ObjectId(example_id), 'class_id': int(class_id)},
            {'$set': {'example_data': new_example_data}}
        )
        if result.modified_count == 1:
            return jsonify({'success': True, 'message': 'Example updated successfully'}), 200
        else:
            return jsonify({'success': False, 'error': 'Example not found or not modified'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/delete_example', methods=['POST'])
def delete_example():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'User not logged in'}), 401

    data = request.json
    class_id = data.get('class_id')
    example_id = data.get('id')

    try:
        result = mongo.db.examples.delete_one({
            '_id': ObjectId(example_id),
            'class_id': int(class_id)
        })
        if result.deleted_count == 1:
            return jsonify({'success': True, 'message': 'Example deleted successfully'}), 200
        else:
            return jsonify({'success': False, 'error': 'Example not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/edit_autoresponse/<class_id>/<autoresponse_id>', methods=['POST'])
def edit_autoresponse(class_id, autoresponse_id):
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'User not logged in'}), 401

    data = request.json
    new_autoresponse_data = data.get('data')

    if not new_autoresponse_data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    try:
        result = mongo.db.autoresponses.update_one(
            {'_id': ObjectId(autoresponse_id), 'class_id': int(class_id)},
            {'$set': {'response': new_autoresponse_data}}
        )
        if result.modified_count == 1:
            return jsonify({'success': True, 'message': 'Autoresponse updated successfully'}), 200
        else:
            return jsonify({'success': False, 'error': 'Autoresponse not found or not modified'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

