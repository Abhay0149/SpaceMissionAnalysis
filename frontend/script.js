// =============================
// Animated Counter
// =============================
function animateValue(id, start, end, duration) {

let obj = document.getElementById(id)
if(!obj) return

let range = end - start
let startTime = null

function step(timestamp){

if(!startTime) startTime = timestamp

let progress = Math.min((timestamp - startTime) / duration, 1)

obj.innerText = Math.floor(progress * range + start)

if(progress < 1){
window.requestAnimationFrame(step)
}

}

window.requestAnimationFrame(step)

}



// =============================
// SUMMARY DATA
// =============================
fetch("/summary")

.then(res => res.json())

.then(data => {

animateValue("missions",0,data.total_missions,1000)

let payloadEl = document.getElementById("payload")
let successEl = document.getElementById("success")

if(payloadEl)
payloadEl.innerText = data.avg_payload + " tons"

if(successEl)
successEl.innerText = data.avg_success + "%"

})

.catch(err => console.log("Summary error:",err))



// =============================
// Mission Types LINE GRAPH
// =============================
let missionChart = null

fetch("/mission-types")

.then(res=>res.json())

.then(data=>{

let labels=[]
let values=[]

data.forEach(item=>{
labels.push(item.name)
values.push(item.count)
})

const ctx=document.getElementById("missionChart").getContext("2d")

if(!ctx) return

if(missionChart){
missionChart.destroy()
}

missionChart = new Chart(ctx,{

type:"line",

data:{
labels:labels,

datasets:[{
label:"Mission Types",
data:values,

borderColor:"#ff6b6b",
backgroundColor:"rgba(255,107,107,0.08)",

fill:true,
tension:0.45,

borderWidth:3,

pointBackgroundColor:"#ff6b6b",
pointBorderColor:"#ffffff",

pointRadius:5,
pointHoverRadius:7
}]
},

options:{

responsive:true,
maintainAspectRatio:false,

plugins:{
legend:{
labels:{
color:"white",
font:{size:14}
}
}
},

scales:{
x:{
ticks:{
color:"white",
font:{size:14}
},
grid:{
color:"rgba(255,255,255,0.05)"
}
},

y:{
ticks:{
color:"white"
},
beginAtZero:true,
grid:{
color:"rgba(255,255,255,0.05)"
}
}

}

}

})

})

.catch(err=>console.log("Mission types error:",err))



// =============================
// 🚀 AI Mission Prediction
// =============================
function predictMission(){

let payloadInput = document.getElementById("payloadInput")
let result = document.getElementById("prediction")

if(!payloadInput || !result) return

let payload = parseFloat(payloadInput.value)

if(isNaN(payload) || payload <= 0){
result.innerText="⚠️ Enter valid payload weight"
return
}

result.innerText="🤖 AI analyzing mission..."

fetch("/predict/" + payload)

.then(res=>res.json())

.then(data=>{

if(data && data.status){

result.innerHTML =
data.status +
"<br><span style='color:#22c55e'>Success: " + data.success + "%</span>" +
"<br><span style='color:#ef4444'>Failure: " + data.failure + "%</span>"

}
else{

result.innerText="⚠️ Prediction failed"

}

})

.catch(err=>{

result.innerText="❌ Server error"
console.log("Prediction error:",err)

})

}