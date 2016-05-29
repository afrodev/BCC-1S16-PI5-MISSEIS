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
    
    //array[1] = array[1].trim();
    //valores = array[1].split(";");
    
    println(p);

    println(valores);

    aviaoX = float(valores[0]) * 0.1;
    aviaoY = float(valores[1]) * 0.1;
    aviaoZ = float(valores[2]) * 1.2;
    
    // 2110.69;8870.51;200.00; 2.55; 0.00;5000.00;5000.00; 0.00; 0.00;
    
    //tiroX =  float(valores[5]) * 0.1;
    //tiroY =  float(valores[6]) * 0.1;
    //tiroZ =  float(valores[7]) * 1.2;
    
    redraw();
    println(p);
}

void draw() {
  background(11);
  
  inc += 0.01; // incrementa o bloco de desenho
  
  /* BLOCO PARA DESENHAR O AVIAO PASSANDO */
  // Cria uma nova matriz (array de numeros) em cima do sistemas de coordenadas, para mudar a posiçao do objeto
  pushMatrix(); 
  
  // Pinta linhas do objeto
  stroke(0, 200, 0);
  fill(0,0, 200); 
  translate(600 - aviaoY, (600 - aviaoZ), -aviaoX); // Muda a posição na tela
  
  // Printa posições do avião pra ter certeza que estão recebendo
  //println(aviaoX);
  //println(aviaoY);
  //println(aviaoZ);
  
  rotateX(-mouseY * 0.01); // roda no eixo x
  rotateY(-mouseX * 0.01); // roda no eixo y
  rotateZ(inc);
  
  // Esfera que recebe como parâmetro um raio
  sphere(10);
  
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
  rotateZ(inc);
  
  sphere(2);
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