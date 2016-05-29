import netP5.*;
import oscP5.*;

import processing.opengl.*;

// Declara a variavel do OSC
OscP5 oscP5;
String p = "";

// Variaveis de controle do avião
float aviaoX;
float aviaoY;
float aviaoZ;

// Variaveis de controle da base
float baseX;
float baseY;
float baseZ;

// Variaveis de controle da tiro
float tiroX;
float tiroY;
float tiroZ;

String []array;
String opcao;
String []valores;

float inc = 0.0; // Esse float muda rotação

void setup() { 
  // Variaveis para inicializar o avião
  aviaoX = 3975.13 * 0.1;
  aviaoY = 7953.53 * 0.1;
  aviaoZ = 500.00 * 1.2;
  
  // Variaveis para inciializar a base
  baseX = 5000.00 * 0.1;
  baseY = 5000.00 * 0.1;
  baseZ = 0 * 0.1;
  
  tiroX = baseX;
  tiroY = baseY;
  tiroZ = baseZ;
   
  // Inicializa o listening da porta 7580 para o OSC
  oscP5 = new OscP5(this, 7580);

  //noStroke(); // Tira a s linha
  //noFill(); // Tira a pintura
  
  
  smooth(4);
  size(650, 650, OPENGL); // OPEN GL permite mexer com coisas em 3D
   
  
}

// Evento que recebe e trata a mensagem do OSC 
void oscEvent(OscMessage theOscMessage) {
    //AVIAOX, AVIAOY, AVIAOZ, AVIAOTEMPOVOANDO, BALAX, BALAY, BALAZ, BALAZ, BALATEMPOVOANDO - Esta no array de valores
    p = theOscMessage.addrPattern();
    String result = p.trim(); //<>//
    valores = result.split(";");
    
    println(p);

    aviaoX = float(valores[0]) * 0.1;
    aviaoY = float(valores[1]) * 0.1;
    aviaoZ = float(valores[2]) * 1.2;
        
    tiroX =  float(valores[5]) * 0.1;
    tiroY =  float(valores[6]) * 0.1;
    tiroZ =  float(valores[7]) * 1.2;
    
    redraw();
    println(p);
}

void draw() {
  background(11);
  
  // Criando eixos Y (de acordo com o processing) 
  beginShape();
  vertex(0, 0, -600);
  vertex(0, 600, -600);
  vertex(0, 0, -600);
  endShape();
  
  
  beginShape();
  vertex(0, 600, -600);
  vertex(600, 600, -600);
  //vertex(0, 600, -600);
  vertex(600, 600, 0);
  vertex(0, 600, 0);
  endShape();

  beginShape();
  vertex(0, 600, 0);
  vertex(0, 600, -600);
  vertex(0, 600, 0);
  endShape();
  
  
  // Calculando o valor do raio
  noFill();
  stroke(30, 30, 30);

  translate(600 - baseY, (600 - baseZ), -baseX);
  sphere(3000 * 0.1);
  

  inc += 0.01; // incrementa o bloco de desenho
  camera(mouseX,mouseY, (height/2) / tan(PI/6), width/2, height/2, 0, 0, 1, 0);
  
  /* BLOCO PARA DESENHAR O AVIAO PASSANDO */
  // Cria uma nova matriz (array de numeros) em cima do sistemas de coordenadas, para mudar a posiçao do objeto
  pushMatrix(); 
  
  // Pinta linhas do objeto
  stroke(0, 200, 0);
  fill(0,0, 200); 
  translate(600 - aviaoY, (600 - aviaoZ), -aviaoX); // Muda a posição na tela
  
  rotateX(-mouseY * 0.01); // roda no eixo x
  rotateY(-mouseX * 0.01); // roda no eixo y
  rotateZ(inc);
  
  // Esfera que recebe como parâmetro um raio
  sphere(8);
  
  // deleta o array de objetos que estão fora da tela do flip
  popMatrix(); 
  
  /* ------------------------------------------------------------------- */
  
  
  /* BLOCO PARA DESENHAR A BASE */
  // Cria uma nova matriz (array de numeros) em cima do sistemas de coordenadas, para mudar a posiçao do objeto
  pushMatrix();
  
  // Pinta a cor das linhas 
  stroke(255, 255, 255);
  fill(0, 0, 0);
  
  translate(600 - baseY, (600 - baseZ), -baseX); // Muda a posição na tela
  
  rotateX(-mouseY * 0.01); // roda no eixo x
  rotateY(-mouseX * 0.01); // roda no eixo y
  //rotateZ(inc);
  
  sphere(10);
  popMatrix(); // deleta o array de objetos que estão fora da tela do flip
 
 /* ------------------------------------------------------------------- */
  // Desenhar a bala 
  pushMatrix();
  stroke(255, 0, 0);
  fill(0, 0, 0);
  
  translate(600 - tiroY, (600 - tiroZ), -tiroX); // Muda a posição na tela
  
  rotateX(-mouseY * 0.01); // roda no eixo x
  rotateY(-mouseX * 0.01); // roda no eixo y
  rotateZ(inc);
  sphere(2);
  
  popMatrix();
}