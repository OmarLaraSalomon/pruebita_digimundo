


//esta funcion va a llamar las otras funciones y sera la unica que s eva a invocar en la ejecucion 
const printCharts = () => {

   
    renderModelsChart() //el primer modelo del chart que es el id  
          

}


//el primer modelo del chart que es el id ModelsChart 
const renderModelsChart =() => {  

    
//se requieren los datos para renderizar el chart
    const data = {
        labels: ['uno', 'dos', 'tres'], //array con las etiquetas a renderizar 

        datasets: [{ //arrasy de objetos, poruqe se pueden jugar cion varios juegos de datos, mas de un objeto 
            //que datos le vamos a dar  //tambie man
            data: [1,20,30],
            borderColor: ['red','green','blue'],
            backgroundColor:['blue','gfreen','red',]
           
        }]
    }

//este es para la renderizacion, tenemos que mandale que se va arederizar y el tipo, obviamente los datos 

        //este es el id          //tipo dona     //datos
    new Chart('modelsChart', { type: 'doughnut', data })
}




printCharts()