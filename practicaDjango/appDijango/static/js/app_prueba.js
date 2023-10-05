
import { fetchPokemonData, fetchPokemonColorData, fetchPokemonStatsData ,getDataColors } from "./helpers_prueba.js";
import {enableEventHandlers} from "./handlers_prueba.js";

//valores por defecto 
Chart.defaults.color = '#fff'
Chart.defaults.borderColor = '#444'



//esta funcion va a llamar las otras funciones y sera la unica que s eva a invocar en la ejecucion 

/*const printCharts = () => { 
    //este va a buscar la api a consumir primero el pokemon y luego el color
    fetchCoastersData('https://pokeapi.co/api/v2/pokemon', 'https://pokeapi.co/api/v2/pokemon-color')
    .then(([name, color]) => { //cuando este todo listo voy a recibir un array  con la primer posicion el pokemon y en segunda el color
        renderModelsChart(name)//este es el que grafica y se les va a pasar con los parametros que querramos
        renderFeaturesChart(color)
        renderYearsChart(name)
        enableEventHandlers(color)
        })



}
*/
//renderizar cada uno de los charts 
const printCharts = () => {
    Promise.all([fetchPokemonData(), fetchPokemonColorData(), fetchPokemonStatsData()])
        .then(([pokemon, colors, stats]) => {
            console.log('Pokémon Names:', pokemon.map(p => p.name));
            console.log('Pokémon Colors:', colors.map(c => c.name));
            console.log('Pokémon Stats:', stats.map(s => s.name));

            renderPastelChart(pokemon);
            renderRadarChart(colors);
            renderLineChart(pokemon, stats);

            enableEventHandlers(colors);
        })
        .catch(error => {
            console.error('ERROR NO SE ENCUENTRAN DATOS:', error);
        });
};







//el primer modelo del chart que es el id pastelChart 
//aceptar una matriz de Pokémon y generar el gráfico.
const renderPastelChart = pokemon => {


//crear un array con todos los modelos 
//con este se sacan los modelos unicos para que no hayan repetidos 
    const uniqueModels = [...new Set(pokemon.map(p => p.name))]; //Obtén una variedad de nombres de Pokémon.

//se requieren los datos para renderizar el chart
    const data = {
        labels: uniqueModels, //array con las etiquetas a renderizar  este es para que no se repitan 
        //arrasy de objetos, poruqe se pueden jugar cion varios juegos de datos, mas de un objeto 



//iterarlo y en cada uno de los modelos encontrar cuantas coinciden             
        datasets: [{
            data: uniqueModels.map(currentModel => {
                const count = pokemon.filter(p => p.name === currentModel).length;
                return count;
            }),

//borderColor: ['red','green','blue'],
//backgroundColor:['blue','green','red',]            

            borderColor: getDataColors(),
            backgroundColor: getDataColors(20)
        }]
    };
//este es para que las leyendas aparezcna a la izquierda y no arriba 
    const options = {
        plugins: {
            legend: { position: 'left' }
        }
    };


//este es para la renderizacion, tenemos que mandale que se va arederizar y el tipo, obviamente los datos 

//estos son objetos que le vamos a pasar

        //este es el id        //tipo dona     //datos   //las opciones
    new Chart('pastelChart', { type: 'doughnut', data, options });
};



const renderRadarChart = colors => {
    // Usaremos solo los primeros 5 colores para este ejemplo
    const selectedColors = colors.slice(0, 10);

    const data = {
        labels: selectedColors.map(c => c.name),
        datasets: [{
            label: 'Color',
            data: selectedColors.map(c => c.name.length), // Esto es problemático, debes cambiarlo
            borderColor: getDataColors(),
            backgroundColor: getDataColors(20)[0]
        }]
    };

    const options = {
        plugins: {
            legend: { display: false }
        },
        scales: {
            r: {
                ticks: { display: false }
            }
        }
    };

    new Chart('radarChart', { type: 'radar', data, options });
};


const renderLineChart = stats => {
    const uniqueStats = [...new Set(stats.map(s => s.name))];
    
    const data = {
        labels: uniqueStats,
        datasets: [{
            data: uniqueStats.map(currentStat => {
                const count = stats.filter(s => s.name === currentStat).length;
                return count;
            }),
            
           
borderColor: getDataColors(),
            backgroundColor: getDataColors(20)
        }]
    };
    
    const options = {
        plugins: {
            legend: { position: 'left' }
        }
    };
    
    new Chart('lineChart', { type: 'line', data, options });
};



printCharts()