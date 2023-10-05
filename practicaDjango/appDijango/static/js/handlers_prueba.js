//gesitonar el evento cuando el usuario interactue con la lista 


import { updateChartData } from "./helpers_prueba.js"

export const enableEventHandlers = colors => {
    console.log('Datos de colores:', colors);

    document.querySelector('#colorOptions').onchange = e => {
        const { value: property, text: label } = e.target.selectedOptions[0];

        console.log('Label seleccionada:', label);
        console.log('Value seleccionada:', property);
//maps es un metodo de arreglos para aplicar una funcion a cada elemento del arreglo
        // Encontrar el color seleccionado en la matriz
        const selectedColor = colors.map(color => color.name === property);

        if (selectedColor) {
            // Llamar a la función para actualizar el gráfico con los datos del color seleccionado
            updateChartData('radarChart', selectedColor, label);
            console.log("Sí pasó el dato", updateChartData);
        } else {
            console.error('No se encontró el color:', property);
        }
    };
};