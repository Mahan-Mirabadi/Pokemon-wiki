import requests
from django.core.cache import cache
import re
from django.shortcuts import render
from django.core.paginator import Paginator

# Helper function to fetch API data
def fetch_data_from_api(url):
    cache_key = f"pokeapi_{url}"  # Generate a unique key for each API call
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data  # Return cached data if it exists
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        
        # Cache the response for 24 hours (86400 seconds)
        cache.set(cache_key, data, timeout=86400)
        
        return data
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None


# Define Pokémon type colors (hex values for the background color)
TYPE_COLORS = {
    'grass': '#9BCC50',
    'poison': '#B97FC9',
    'fire': '#F08030',
    'water': '#6890F0',
    'bug': '#A8B820',
    'normal': '#A8A878',
    'electric': '#F8D030',
    'ground': '#E0C068',
    'fairy': '#EE99AC',
    'fighting': '#C03028',
    'psychic': '#F85888',
    'rock': '#B8A038',
    'ghost': '#705898',
    'dragon': '#6F35FC',
    'dark': '#705848',
    'steel': '#B8B8D0',
    'ice': '#98D8D8',
    'unknown': '#68A090',
    'shadow': '#000000',
    'flying': '#87CEEB',  # Light cyan color for better visibility
    # Add more as needed
}

# View to list Pokémon with pagination
def pokemon_list(request):
    url = 'https://pokeapi.co/api/v2/pokemon?limit=1000'  # Reduced limit for lighter load
    data = fetch_data_from_api(url)
    
    if not data:  # Handle API error
        return render(request, 'wiki/pokemon_list.html', {'pokemons': [], 'error': 'Failed to load data.'})
    
    pokemons = data['results']
    
    # Paginate the list (50 Pokémon per page)
    paginator = Paginator(pokemons, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'wiki/pokemon_list.html', {'page_obj': page_obj})

# Helper function to clean the Pokémon description
def clean_description(description):
    cleaned_description = re.sub(r'[\n\r\f]', ' ', description)  # Replace special characters with spaces
    cleaned_description = cleaned_description.replace('POKéMON', 'Pokémon')
    return cleaned_description

# View to show Pokémon details
def pokemon_detail(request, name):
    # Fetch basic Pokémon details
    url = f'https://pokeapi.co/api/v2/pokemon/{name}/'
    pokemon_data = fetch_data_from_api(url)
    
    if not pokemon_data:  # Handle API error
        return render(request, 'wiki/pokemon_detail.html', {'error': 'Failed to load Pokémon data.'})
    
    # Convert height and weight to meters and kilograms
    height_in_meters = pokemon_data['height'] * 0.1
    weight_in_kg = pokemon_data['weight'] * 0.1
    
    # Fetch species data for description, evolution, and Pokédex number
    species_url = pokemon_data['species']['url']
    species_data = fetch_data_from_api(species_url)
    
    # Extract English description (flavor text) and clean it
    raw_description = next((entry['flavor_text'] for entry in species_data['flavor_text_entries'] if entry['language']['name'] == 'en'), 'No description available')
    description = clean_description(raw_description)
    
    # Extract Pokédex number and format with leading zeros
    pokedex_number = f"#{species_data['id']:04d}"
    
    # Fetch evolution chain
    evolution_chain_url = species_data['evolution_chain']['url']
    evolution_chain_data = fetch_data_from_api(evolution_chain_url)
    
    # Function to traverse evolution chain and collect evolutions
    def get_evolutions(chain):
        evolutions = []
        
        def traverse_evolution(chain):
            current_name = chain['species']['name']
            # Fetch data for each species to get the sprite and name
            current_pokemon_data = fetch_data_from_api(f"https://pokeapi.co/api/v2/pokemon/{current_name}/")
            evolutions.append({
                'name': current_name,
                'sprite': current_pokemon_data['sprites']['front_default']
            })
            if chain['evolves_to']:
                for evolution in chain['evolves_to']:
                    traverse_evolution(evolution)
        
        traverse_evolution(chain)
        return evolutions
    
    evolutions = get_evolutions(evolution_chain_data['chain'])
    
    # Extract stats
    stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']}
    
    # Fetch weaknesses based on types
    weaknesses = set()
    weaknesses_with_colors = []
    types_with_colors = []
    for type_ in pokemon_data['types']:
        type_name = type_['type']['name']
        type_color = TYPE_COLORS.get(type_name, '#FFFFFF')  # Default to white if type not found
        types_with_colors.append({'name': type_name, 'color': type_color})
        type_data = fetch_data_from_api(type_['type']['url'])
        if type_data:
            for damage_relation in type_data['damage_relations']['double_damage_from']:
                damage_name = damage_relation['name']
                damage_color = TYPE_COLORS.get(damage_name, '#FFFFFF')  # Default to white if type not found
                weaknesses_with_colors.append({'name': damage_name, 'color': damage_color})
                weaknesses.add(damage_name)
    
    # Extract sprite (image URL)
    sprite_url = pokemon_data['sprites']['front_default']
    
    # Extract additional data
    abilities = [ability['ability']['name'] for ability in pokemon_data['abilities']]
    types = [type_['type']['name'] for type_ in pokemon_data['types']]
    
    return render(request, 'wiki/pokemon_detail.html', {
        'pokemon': pokemon_data,
        'abilities': abilities,
        'types_with_colors': types_with_colors,
        'height': round(height_in_meters, 1),
        'weight': round(weight_in_kg, 1),
        'sprite_url': sprite_url,
        'description': description,
        'stats': stats,
        'evolutions': evolutions,
        'weaknesses_with_colors': weaknesses_with_colors,
        'pokedex_number': pokedex_number
    })
