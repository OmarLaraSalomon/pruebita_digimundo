//esta va a recibir las urls en array, en este caso vams a iterar las url que le mandemos y hacemos una llamada de ajax
//Una promesa es un objeto que representa un valor que puede estar disponible ahora, en el futuro o nunca

//=> es una funcion  procediendo por la lista de argumentos
export const fetchPokemonData = () => {
    const apiUrl = 'https://pokeapi.co/api/v2/pokemon';
    
    return fetch(apiUrl) //: Realice una solicitud a la URL de la API. fetch es bucar en base 
//el .then devuelve una promesa 
        .then(response => response.json()) //Convierte la respuesta al formato JSON.
        .then(data => data.results) //acceda a la propiedad results de los datos, que contiene una matriz de objetos con información sobre los Pokémon.
        .catch(error => { //un try catch para ver las excepciones 
            console.error('Error fetching Pokémon data:', error);
            throw error;
        });
};


export const fetchPokemonColorData = () => {
    const apiUrl = 'https://pokeapi.co/api/v2/pokemon-color';
    
    return fetch(apiUrl)
        .then(response => response.json())
        .then(data => data.results)
        .catch(error => {
            console.error('Error fetching Pokémon color data:', error);
            throw error;
        });
};



export const fetchPokemonStatsData = () => {
    const apiUrl = 'https://pokeapi.co/api/v2/stat';

    return fetch(apiUrl)
        .then(response => response.json())
        .then(data => data.results)
        .catch(error => {
            console.error('Error fetching Pokémon color data:', error);
            throw error;
        });
};


//funcion para retornar el array de colores, puede recibir opacidad encaso de que exista me retorna y se le va a concatenar lo de la opacidad, si no se retorna el color sini opacidad 
export const getDataColors = opacity => {
    const colors = ['#7448c2', '#21c0d7', '#d99e2b', '#cd3a81', '#9c99cc', '#e14eca', '#ffffff', '#ff0000', '#d6ff00', '#0038ff']
    return colors.map(color => opacity ? `${color + opacity}` : color)
}




//forma de mutar datros
//le mandamos el id, los nuevos datos y las etiqaeutas

export const updateChartData = (chartId, data, label) => {
    const chart = Chart.getChart(chartId);
    console.log('Chart:', chartId);

    if (chart) {
        chart.data.datasets[0].data = data;
        chart.data.datasets[0].label = label;
        chart.update();
    } else {
        console.error('El gráfico no fue encontrado:', chartId);
        console.error('No se ha actualizado.');
    }
};

/*export const getCoastersByAbility = (pokemon, abilities) => {
    const result = Object.values(abilities).map(ability => {
        return pokemon.filter(pokemonItem => pokemonItem.abilities.some(pAbility => pAbility.ability.name === ability.name)).length;
    });
    return result;
}; */