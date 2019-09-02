let rutine = null;
let actual_exer = null;
let time_exer = null;
let good_exer = true;

let video = null;
let socket = null;
let net = null;
let ctx = null;



window.addEventListener("load", function() {

    ctx = document.getElementById("canvas").getContext("2d");
    get_rutine();
    load_camera();
    load_poseNet();
    start_rutine();

}, false);


async function start_rutine() {
    socket = io();


    setInterval(() => {

        if (video != null || net != null) {

            detectar_puntos((pose) => {
                pintar(pose)
                envio_video(socket, pose)
            })
        }

    }, 100)
}

async function load_poseNet() {
    net = await posenet.load({
        architecture: 'ResNet50',
        outputStride: 32,
        inputResolution: 257,
        quantBytes: 2
    });
}

//carga la camara e inicia la captura, retorna la camara para la funcion callback
async function load_camera() {
    if (navigator.getUserMedia) {
        navigator.getUserMedia({
                audio: false,
                video: {
                    width: 640,
                    height: 480
                }
            }, //paramettres
            function(stream) {
                video = document.querySelector('video');
                video.width = 640;
                video.height = 480;
                video.srcObject = stream;

                video.onloadedmetadata = function(e) {
                    video.play()

                    //console.log(detectar_puntos(video))

                };
            }, //succed
            function(err) {
                console.log("The following error occurred: " + err.name);
            }
        ); //failure
    } else {
        console.log("getUserMedia not supported");
    }
}

// recibe el video y la red para detectar los puntos clave y los retorna por medio del callback
async function detectar_puntos(callback) {

    const pose = await net.estimateSinglePose(video, {
        flipHorizontal: false
    });
    callback(pose)
}

const pintar = (pose) => {
    ctx.drawImage(video, 0, 0, 640, 480);
    var puntos_clave = pose.keypoints;
    for (var i = puntos_clave.length - 1; i >= 0; i--) {
        drawCoordinates(puntos_clave[i].position);
    }
}


function drawCoordinates(position) {
    x = position.x;
    y = position.y;
    var pointSize = 3; // Change according to the size of the point.
    ctx.fillStyle = "#ff2626"; // Red color
    ctx.beginPath(); //Start path
    ctx.arc(x, y, pointSize, 0, Math.PI * 2, true); // Draw a point using the arc function of the canvas with a point structure.
    ctx.fill(); // Close the path and fill.
}


async function get_rutine() {

    fetch("http://127.0.0.1:5000/get_rutine/" + 1).then((rutineJson) => {
        rutineJson.json().then((data) => {
            rutine = data
            actual_exer = 0;
            change_img()

        })

    })



}

//envia por socket io el video
const envio_video = (so, pose) => {
    const pose_new = Object.assign({ model: "" + rutine.rutine[actual_exer].id_exercise }, pose);
    const pose_json = JSON.stringify(pose_new)
        //console.log(pose_json)
    so.emit('stream', pose_json, callback = retorno);
}



const change_img = () => {
    const img = document.getElementById("imagen-muestra")
    img.src = "./static/images/" + rutine.rutine[actual_exer].imagen

}

const retorno = (message) => {


    if (message === "true") {
        good_exer = true
    } else {
        good_exer = false
    }

    console.log(good_exer)

    if (time_exer == null & good_exer) {
        time_exer = new Date();
    } else if (good_exer) {
        let current_time = new Date()
        document.getElementById("banner").innerHTML = "Doing well"
        let diferenciaa = (current_time.getTime() - time_exer.getTime()) / 1000
        if (diferenciaa >= rutine.rutine[actual_exer].duration) {
            document.getElementById("banner").innerHTML = "Succesfull - Next exercise"
            time_exer = null
            good_exer = !good_exer

            actual_exer++

            if (actual_exer === rutine.num_exercises) {
                window.location.href = "/succed";

            } else {
                change_img()
            }


        }
    } else {
        document.getElementById("banner").innerHTML = "You are doing a wrong exercise"
        time_exer = null
    }

}

async function send_json() {
    net = await posenet.load({
        architecture: 'ResNet50',
        outputStride: 32,
        inputResolution: 257,
        quantBytes: 2
    });

    socket = io();

    if (net != null) {

        const img = document.getElementById("imagen-muestra")
        const pose = await net.estimateSinglePose(img, {
            flipHorizontal: false
        });
        console.log(pose)
        socket.emit('modelo', pose);

    }


}