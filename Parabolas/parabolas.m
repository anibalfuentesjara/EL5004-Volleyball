% Parametros fijos
global altura_red distancia_x_omni altura_omni
altura_red = 2.6;
distancia_x_omni = -10;
altura_omni = 1;

% Parametros variables
distancia_persona = 3;
altura_persona = 1;
altura_sobre_red = 0.5;

% Calculo de parabola mediante polyfit
parabola = calcular_parabola(distancia_persona, altura_persona, altura_sobre_red);

% Vectores x e y de trayectoria de la parabola
x = distancia_x_omni:0.1:distancia_persona;
y = parabola(1)*x.^2 + parabola(2)*x + parabola(3);

% Pendiente de la parabola en el punto de lanzamiento.
m = 2*parabola(1)*distancia_x_omni + parabola(2);

% Angulo de elevacion
angulo_rad = atan(m);
angulo = angulo_rad * 180/pi;

% Velocidad inicial
gravedad = -9.81;
v_0 = sqrt((0.5*gravedad*(distancia_persona-distancia_x_omni)^2)/...
    (cos(angulo_rad)^2*((altura_persona-altura_omni)-...
    tan(angulo_rad)*(distancia_persona-distancia_x_omni))));

% Imprimir en pantalla angulo de elevacion y velocidad inicial necesaria
velocidad = strcat('Velocidad necesaria (m/s):',string(v_0));
ang = strcat('Angulo necesario (°):',string(angulo));
disp(velocidad)
disp(ang)

%Grafico dinamico de la trayectoria
figure()
hold on
xlim([-10,10])
ylim([0,max(y)+0.3])
bar([distancia_persona],[altura_persona],'r','BarWidth', 0.3)
bar([0],[altura_red],'k','BarWidth', 0.2)
bar([distancia_x_omni],[altura_omni],'g','BarWidth', 0.3)
%Identificadores
txt1 = '\leftarrow Omniwrist'; text(distancia_x_omni,altura_omni,txt1)
txt2 = '\leftarrow Malla'; text(0,altura_red,txt2)
txt3 = char(strcat("\leftarrow Recepción.Distancia:",string(distancia_persona), 'm')); text(distancia_persona,altura_persona,txt3)
%Texto de velocidad y angulo
text(max(x),max(y),char(velocidad))
text(max(x),max(y)-0.14,char(ang))
comet(x,y)
hold off

function parabola = calcular_parabola(distancia_persona, altura_persona, altura_sobre_red)
%Calcula la parabola que debe seguir el balon
global altura_red distancia_x_omni altura_omni
punto_1 = [distancia_x_omni, altura_omni];
punto_2 = [0, altura_red+altura_sobre_red];
punto_3 = [distancia_persona, altura_persona];
puntos_x = [punto_1(1), punto_2(1), punto_3(1)];
puntos_y = [punto_1(2), punto_2(2), punto_3(2)];
p = polyfit(puntos_x, puntos_y, 2);
parabola = p;
end