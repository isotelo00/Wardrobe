from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

# Dummy data for demonstration
wardrobe = {
    'items': [
        {'name': 'Blue Shirt', 'category': 'Tops', 'type': 'Shirt', 'color': '#0000FF'},
        {'name': 'Black Jeans', 'category': 'Bottoms', 'type': 'Jeans', 'color': '#000000'},
        {'name': 'White Sneakers', 'category': 'Footwear', 'type': 'Sneakers', 'color': '#FFFFFF'},
        {'name': 'Silver Watch', 'category': 'Accessories', 'type': 'Watch', 'color': '#C0C0C0'},
        {'name': 'Red Sweater', 'category': 'Tops', 'type': 'Sweater', 'color': '#FF0000'},
        {'name': 'Khaki Pants', 'category': 'Bottoms', 'type': 'Pants', 'color': '#C3B091'},
        {'name': 'Brown Boots', 'category': 'Footwear', 'type': 'Boots', 'color': '#8B4513'},
        {'name': 'Leather Belt', 'category': 'Accessories', 'type': 'Belt', 'color': '#A0522D'},
        {'name': 'White T-Shirt', 'category': 'Tops', 'type': 'T-Shirt', 'color': '#FFFFFF'},
        {'name': 'Blue Shorts', 'category': 'Bottoms', 'type': 'Shorts', 'color': '#0000FF'},
        {'name': 'Black Sneakers', 'category': 'Footwear', 'type': 'Sneakers', 'color': '#000000'},
        {'name': 'Silver Bracelet', 'category': 'Accessories', 'type': 'Bracelet', 'color': '#C0C0C0'},
        {'name': 'Green Hoodie', 'category': 'Tops', 'type': 'Hoodie', 'color': '#008000'},
        {'name': 'Denim Jacket', 'category': 'Tops', 'type': 'Jacket', 'color': '#4169E1'},
        {'name': 'Black Leggings', 'category': 'Bottoms', 'type': 'Leggings', 'color': '#000000'},
        {'name': 'Brown Loafers', 'category': 'Footwear', 'type': 'Loafers', 'color': '#8B4513'},
        {'name': 'Red Scarf', 'category': 'Accessories', 'type': 'Scarf', 'color': '#FF0000'},
        {'name': 'Yellow Polo', 'category': 'Tops', 'type': 'Polo', 'color': '#FFFF00'},
        {'name': 'Gray Sweatpants', 'category': 'Bottoms', 'type': 'Sweatpants', 'color': '#808080'},
        {'name': 'White Sandals', 'category': 'Footwear', 'type': 'Sandals', 'color': '#FFFFFF'},
        {'name': 'Black Sunglasses', 'category': 'Accessories', 'type': 'Sunglasses', 'color': '#000000'},
        {'name': 'Purple Blouse', 'category': 'Tops', 'type': 'Blouse', 'color': '#800080'},
        {'name': 'Navy Skirt', 'category': 'Bottoms', 'type': 'Skirt', 'color': '#000080'},
        {'name': 'Brown Oxfords', 'category': 'Footwear', 'type': 'Oxfords', 'color': '#8B4513'},
        {'name': 'Silver Earrings', 'category': 'Accessories', 'type': 'Earrings', 'color': '#C0C0C0'},
        {'name': 'Pink Dress', 'category': 'Tops', 'type': 'Dress', 'color': '#FFC0CB'},
        {'name': 'Beige Chinos', 'category': 'Bottoms', 'type': 'Chinos', 'color': '#F5F5DC'},
        {'name': 'Black Heels', 'category': 'Footwear', 'type': 'Heels', 'color': '#000000'},
        {'name': 'Gold Necklace', 'category': 'Accessories', 'type': 'Necklace', 'color': '#FFD700'},
        {'name': 'Striped Sweater', 'category': 'Tops', 'type': 'Sweater', 'color': '#FFFFFF'},
        {'name': 'Blue Joggers', 'category': 'Bottoms', 'type': 'Joggers', 'color': '#0000FF'},
        {'name': 'White Canvas Shoes', 'category': 'Footwear', 'type': 'Shoes', 'color': '#FFFFFF'}
    ],
    'outfits': [
        {
            'tops': 'Red Sweater',
            'bottoms':'Khaki Pants',
            'footwear':'Brown Boots',
            'accessories': 'Leather Belt'
        },
        {
            'tops': 'Green Hoodie',
            'bottoms':'Denim Jacket',
            'footwear':'Black Leggings',
            'accessories':'Brown Loafers'
        }
    ]
}

def generate_complementary_outfit(top):
    selected_top = get_item_by_name(top)
    complementary_bottom = find_complementary_item(selected_top, 'Bottoms')
    complementary_footwear = find_complementary_item(selected_top, 'Footwear')
    complementary_accessory = find_complementary_item(selected_top, 'Accessories')
    
    outfit = {
        'tops': selected_top['name'],
        'bottoms': complementary_bottom['name'],
        'footwear': complementary_footwear['name'],
        'accessories': complementary_accessory['name']
    }
    print(outfit)
    return outfit

def get_item_by_name(item_name):
    for item in wardrobe['items']:
        if item['name'] == item_name:
            return item
    return None

def filter_items_by_category(category):
    filtered_items = []
    for item in wardrobe['items']:
        if item['category'] == category:
            filtered_items.append(item)
    return filtered_items

def find_complementary_item(item, category):
    category_items = filter_items_by_category(category)
    return min(category_items, key=lambda x: color_distance(item['color'], x['color']))

def color_distance(color1, color2):
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)
    
    distance = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
    
    return distance

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_outfit', methods=['GET', 'POST'])
def generate_outfit():
    if request.method == 'POST':
        top = request.form.get('top')
        outfit = generate_complementary_outfit(top)
        wardrobe['outfits'].append(outfit)
        return render_template('view_outfits.html', outfits=wardrobe['outfits'])
    else:
        tops = filter_items_by_category('Tops')
        return render_template('generate_outfit.html', tops=tops)


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['item-name']
        category = request.form['category']
        type = request.form['type']
        color = request.form['color']

        wardrobe['items'].append({'name': str(name), 'category': str(category), 'type': str(type), 'color': str(color)})

        category_filter = request.form.get('category_filter')
        filtered_items = [item for item in wardrobe['items'] if not category_filter or item['category'] == category_filter]
        return render_template('view_items.html', filtered_items=filtered_items, category_filter=category_filter)

    return render_template('add_item.html')



@app.route('/view_items', methods=['GET', 'POST'])
def view_items():
    category_filter = request.form.get('category_filter')
    filtered_items = [item for item in wardrobe['items'] if not category_filter or item['category'] == category_filter]
    return render_template('view_items.html', filtered_items=filtered_items, category_filter=category_filter)


@app.route('/create_outfit', methods=['GET', 'POST'])
def create_outfit():
    if request.method == 'POST':
        tops = request.form.get('tops')
        bottoms = request.form.get('bottoms')
        footwear = request.form.get('footwear')
        accessories = request.form.get('accessories')

        outfit = {
            'tops': tops,
            'bottoms': bottoms,
            'footwear': footwear,
            'accessories': accessories
        }

        wardrobe['outfits'].append(outfit)

        return render_template('view_outfits.html', outfits=wardrobe['outfits'])

    tops = [item for item in wardrobe['items'] if item['category'] == 'Tops']
    bottoms = [item for item in wardrobe['items'] if item['category'] == 'Bottoms']
    footwear = [item for item in wardrobe['items'] if item['category'] == 'Footwear']
    accessories = [item for item in wardrobe['items'] if item['category'] == 'Accessories']

    return render_template('create_outfit.html', tops=tops, bottoms=bottoms, footwear=footwear, accessories=accessories)



@app.route('/view_outfits')
def view_outfits():
    print(wardrobe['outfits'])
    return render_template('view_outfits.html', outfits=wardrobe['outfits'])


if __name__ == '__main__':
    app.run(debug=True)
    print("Please load this webpage by opening http://localhost:5000/")
