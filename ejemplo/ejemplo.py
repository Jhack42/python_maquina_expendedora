from IPython.display import HTML, display

html = r"""
<!DOCTYPE html>
<html>
<head>

<style>

body{
    margin:0;
    background:#202124;
    font-family:Arial;
}

/*======================*/
/* MAQUINA */
/*======================*/

.maquina{

    width:950px;
    height:650px;

    margin:30px auto;

    background:linear-gradient(#d8d8d8,#bdbdbd);

    border-radius:30px;

    padding:20px;

    display:flex;

    box-shadow:0 0 40px black;

    animation:rgb 5s infinite;

}

@keyframes rgb{

0%{box-shadow:0 0 30px #00bfff;}
25%{box-shadow:0 0 40px #00ff90;}
50%{box-shadow:0 0 40px #ff0090;}
75%{box-shadow:0 0 40px #ffcc00;}
100%{box-shadow:0 0 30px #00bfff;}

}


/*======================*/
/* VITRINA */
/*======================*/

.vitrina{

    flex:2;

    background:rgba(255,255,255,.85);

    border-radius:20px;

    padding:20px;

    position:relative;

    overflow:hidden;

}

/* reflejo */

.vitrina:before{

content:"";

position:absolute;

left:-200px;

top:0;

width:120px;

height:100%;

background:rgba(255,255,255,.35);

transform:skewX(-25deg);

animation:brillo 5s infinite;

}

@keyframes brillo{

0%{left:-200px;}
100%{left:120%;}

}

.grid{

display:grid;

grid-template-columns:repeat(2,1fr);

gap:20px;

}

.producto{

background:white;

border-radius:15px;

padding:10px;

text-align:center;

transition:.3s;

cursor:pointer;

}

.producto:hover{

transform:translateY(-8px) scale(1.04);

box-shadow:0 10px 25px rgba(0,0,0,.3);

}

.producto img{

width:120px;
height:120px;
object-fit:contain;

}

.nombre{

font-size:22px;
font-weight:bold;

}

.precio{

color:#1976d2;
font-size:20px;

}


/*======================*/
/* PANEL DERECHO */
/*======================*/

.panel{

width:280px;

margin-left:20px;

display:flex;

flex-direction:column;

}

/*======================*/
/* LED */
/*======================*/

.led{

background:black;

color:#00ff66;

font-family:Courier New;

font-size:22px;

padding:15px;

border-radius:10px;

height:70px;

display:flex;

justify-content:center;

align-items:center;

box-shadow:0 0 20px #00ff66 inset;

margin-bottom:20px;

}

/*======================*/
/* TECLADO */
/*======================*/

.teclado{

display:grid;

grid-template-columns:repeat(3,1fr);

gap:10px;

}

.tecla{

background:#424242;

color:white;

padding:18px;

text-align:center;

border-radius:10px;

cursor:pointer;

font-size:22px;

transition:.15s;

user-select:none;

}

.tecla:hover{

background:#616161;

}

.tecla:active{

transform:scale(.9);

background:#00c853;

}

/*======================*/
/* SALDO */
/*======================*/

.saldo{

margin-top:25px;

font-size:28px;

font-weight:bold;

text-align:center;

color:white;

}

/*======================*/
/* BANDEJA */
/*======================*/

.bandeja{

margin-top:auto;

background:#111;

height:80px;

border-radius:15px;

display:flex;

justify-content:center;

align-items:center;

font-size:28px;

color:white;

box-shadow: inset 0 0 20px black;

}

</style>

</head>

<body>

<div class="maquina">

<div class="vitrina">

<div class="grid">

<div class="producto">
<img src="https://cdn-icons-png.flaticon.com/512/3081/3081985.png">
<div class="nombre">Chocolate</div>
<div class="precio">S/.2.00</div>
</div>

<div class="producto">
<img src="https://cdn-icons-png.flaticon.com/512/2553/2553691.png">
<div class="nombre">Galleta</div>
<div class="precio">S/.3.00</div>
</div>

<div class="producto">
<img src="https://cdn-icons-png.flaticon.com/512/1046/1046784.png">
<div class="nombre">Refresco</div>
<div class="precio">S/.5.00</div>
</div>

<div class="producto">
<img src="https://cdn-icons-png.flaticon.com/512/1046/1046751.png">
<div class="nombre">Papas</div>
<div class="precio">S/.4.00</div>
</div>

</div>

</div>

<div class="panel">

<div class="led" id="led">
BIENVENIDO
</div>

<div class="teclado">

<div class="tecla">1</div>
<div class="tecla">2</div>
<div class="tecla">3</div>

<div class="tecla">4</div>
<div class="tecla">5</div>
<div class="tecla">6</div>

<div class="tecla">7</div>
<div class="tecla">8</div>
<div class="tecla">9</div>

<div class="tecla">*</div>
<div class="tecla">0</div>
<div class="tecla">#</div>

</div>

<div class="saldo">

💰 S/.20.00

</div>

<div class="bandeja">

📦

</div>

</div>

</div>

<script>

const mensajes=[
"BIENVENIDO",
"INSERTE MONEDAS",
"SELECCIONE PRODUCTO",
"GRACIAS POR VISITAR"
];

let i=0;

setInterval(()=>{

document.getElementById("led").innerHTML=mensajes[i];

i++;

if(i>=mensajes.length)
i=0;

},2000);

</script>

</body>
</html>
"""

display(HTML(html))