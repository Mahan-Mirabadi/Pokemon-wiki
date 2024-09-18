document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('#search-form');
  const queryInput = document.querySelector('#query');
  const dataTableBody = document.querySelector('#datatable tbody');
  const errorMessage = document.querySelector('#error-message');

  queryInput.addEventListener('input', async function(event) {
      const query = queryInput.value.trim();
      if (query) {
          try {
              const response = await fetch(`/wiki/search/?query=${query}`, {
                  headers: {
                      'X-Requested-With': 'XMLHttpRequest'
                  }
              });
              const data = await response.json();

              if (data.pokemon_data) {
                  dataTableBody.innerHTML = data.pokemon_data.map(pokemon => `
                      <tr>
                          <td>${pokemon.name}</td>
                          <td>${pokemon.height}</td>
                          <td>${pokemon.weight}</td>
                          <td>${pokemon.types.join(', ')}</td>
                      </tr>
                  `).join('');
                  errorMessage.textContent = ''; // Clear error message
              } else {
                  dataTableBody.innerHTML = '';
                  errorMessage.textContent = data.error_message || 'No data found';
              }
          } catch (error) {
              console.error('Error fetching Pokémon data:', error);
          }
      } else {
          dataTableBody.innerHTML = '';
          errorMessage.textContent = ''; // Clear error message
      }
  });
});
