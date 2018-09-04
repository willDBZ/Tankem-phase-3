#Selon http://www.panda3d.org/manual/index.php/Accessing_Config_Vars_in_a_Program
#Les op

fullscreen #f

#On utiliser openGL car tinydisplay (qui est par défaut) est mal installé et produit des bugs
#pandadx9 n'est pas installé
#pandadx8 change la physique
#pandagl fonctionne partout... Vive OpenGL!
load-display pandagl
win-size 1024 600
window-title Tankem
undecorated False
sync-video True

#Si vous avex des problèmes de performance
show-frame-rate-meter False