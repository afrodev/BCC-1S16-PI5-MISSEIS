import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import netP5.*; 
import oscP5.*; 
import processing.opengl.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class drawing_sphere extends PApplet {






// Declara a variavel do OSC
OscP5 oscP5;
String p = "";

// Variaveis de controle do avi\u00e3o
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


float aviaoTempoVoando;
float balasAtiradas;
float balaTempoVoando;
int acertou;

float inc = 0.0f; // Esse float muda rota\u00e7\u00e3o

public void setup() { 
  // Variaveis para inicializar o avi\u00e3o
  aviaoX = 3975.13f;
  aviaoY = 7953.53f;
  aviaoZ = 500.00f;
  
  // Variaveis para inciializar a base
  baseX = 5000.00f * 0.1f;
  baseY = 5000.00f * 0.1f;
  baseZ = 0 * 0.1f;
  
  tiroX = baseX;
  tiroY = baseY;
  tiroZ = baseZ;
   
  // Inicializa o listening da porta 7580 para o OSC
  oscP5 = new OscP5(this, 7580);

  
   // OPEN GL permite mexer com coisas em 3D
  
}

// Evento que recebe e trata a mensagem do OSC 
public void oscEvent(OscMessage theOscMessage) {
    //AVIAOX, AVIAOY, AVIAOZ, AVIAOTEMPOVOANDO, BALASATIRADAS, BALAX, BALAY, BALAZ, BALATEMPOVOANDO, ACERTOU - Esta no array de valores
    p = theOscMessage.addrPattern();
    String result = p.trim(); //<>//
    valores = result.split(";");
    
    println(p);

    aviaoX = PApplet.parseFloat(valores[0]); //<>//
    aviaoY = PApplet.parseFloat(valores[1]);
    aviaoZ = PApplet.parseFloat(valores[2]);
        
    tiroX =  PApplet.parseFloat(valores[5]);
    tiroY =  PApplet.parseFloat(valores[6]);
    tiroZ =  PApplet.parseFloat(valores[7]);
    
    aviaoTempoVoando = PApplet.parseFloat(valores[3]);
    balasAtiradas = PApplet.parseFloat(valores[4]);
    balaTempoVoando = PApplet.parseFloat(valores[8]);
    acertou = PApplet.parseInt(valores[9]);
    

    
    redraw();
    println(p);
}

public void draw() {
  background(11);
  fill(0);
  
  // Criando eixos Y (de acordo com o processing) 
  beginShape();
  vertex(0, 0, -500);
  vertex(0, 500, -500);
  vertex(0, 0, -500);
  endShape();
  
  
  beginShape();
  vertex(-500, 500, -500);
  vertex(500, 500, -500);
  vertex(0, 500, -500);
  endShape();

  beginShape();
  vertex(0, 500, 0);
  vertex(0, 500, -1000);
  vertex(0, 500, 0);
  endShape();
  
  beginShape();
  vertex(-500, 500, -1000);
  vertex(500, 500, -1000);
  vertex(500, 500, 0);
  vertex(-500, 500, 0);
  vertex(-500, 500, -1000);
  endShape();
  
  // Calculando o valor do raio
  noFill();
  stroke(30, 30, 30);

  translate(500 - baseY, (500 - baseZ), -baseX);
  sphere(3000 * 0.1f);
  
  inc += 0.01f; // incrementa o bloco de desenho
  
  camera(mouseX + 500,mouseY, (height/2) / tan(PI/6), width/2, height/2, 0, 0, 1, 0);
  
  /* BLOCO PARA DESENHAR O AVIAO PASSANDO */
  // Cria uma nova matriz (array de numeros) em cima do sistemas de coordenadas, para mudar a posi\u00e7ao do objeto
  pushMatrix(); 
  
  // Pinta linhas do objeto
  stroke(0, 200, 0);
  fill(0,0, 200); 
  translate(500 - aviaoY * 0.1f, (500 - aviaoZ * 1.2f), -aviaoX * 0.1f); // Muda a posi\u00e7\u00e3o na tela
  
  rotateX(-mouseY * 0.01f); // roda no eixo x
  rotateY(-mouseX * 0.01f); // roda no eixo y
  rotateZ(inc);
  
  // Esfera que recebe como par\u00e2metro um raio
  sphere(8);
  
  // deleta o array de objetos que est\u00e3o fora da tela do flip
  popMatrix(); 
  
  /* ------------------------------------------------------------------- */
  
  
  /* BLOCO PARA DESENHAR A BASE */
  // Cria uma nova matriz (array de numeros) em cima do sistemas de coordenadas, para mudar a posi\u00e7ao do objeto
  pushMatrix();
  
  // Pinta a cor das linhas 
  stroke(255, 255, 255);
  fill(0, 0, 0);
  
  translate(500 - baseY, (500 - baseZ), -baseX); // Muda a posi\u00e7\u00e3o na tela
  
  rotateX(-mouseY * 0.01f); // roda no eixo x
  rotateY(-mouseX * 0.01f); // roda no eixo y
  //rotateZ(inc);
  
  sphere(10);
  popMatrix(); // deleta o array de objetos que est\u00e3o fora da tela do flip
 
 /* ------------------------------------------------------------------- */
  // Desenhar a bala 
  pushMatrix();
  stroke(255, 0, 0);
  fill(0, 0, 0);
  
  translate(500 - tiroY * 0.1f, (500 - tiroZ * 1.2f), -tiroX * 0.1f); // Muda a posi\u00e7\u00e3o na tela
  
  rotateX(-mouseY * 0.01f); // roda no eixo x
  rotateY(-mouseX * 0.01f); // roda no eixo y
  rotateZ(inc);
  sphere(2);
  
  popMatrix();
  
  fill(255);
  textSize(90);
  
  /* Escreve na tela */
  text("AVIAO - X: " + aviaoX + " | Y: " + aviaoY + " | Z: " + aviaoZ + "", -2000, -100, -1900);
  text("AVIAO INSTANTE t: " + aviaoTempoVoando + " s" , -2000, 0, -1900);
  text("BALA - X: " + tiroX + " | Y: " + tiroY + " | Z: " + tiroZ + "", -2000, 100, -1900);
  text("BALA INSTANTE t: " + balaTempoVoando + " s" , -2000, 200, -1900);
  text("BALAS ATIRADAS:" + balasAtiradas, -2000, 300, -1900);
  text("ACERTOU:" + acertou, -2000, 400, -1900);

}
  public void settings() {  size(650, 650, OPENGL);  smooth(4); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "drawing_sphere" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
