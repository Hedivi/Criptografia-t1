#!/bin/bash

TYPES=("rsa" "aes" "proposed")
ENTRADAS=("1-musa_consolatrix.txt" "2-braz_cubas_I.txt" "3-dom_casmurro.txt" "4-la_plebe_III.txt")
REPETICOES=31

for type in "${TYPES[@]}"; do
    for entrada in "${ENTRADAS[@]}"; do
        echo "=== type= $type | entrada=$entrada ==="

        for ((i=1; i<=REPETICOES; i++)); do
            echo "Execução $i/$REPETICOES"
            python3 main.py --type $type --open_text "entradas/$entrada" --cipher_text "cifras/$type-$entrada-$i.txt" --key "keys/key-$type.txt" --cipher True
        done
    done
done

for type in "${TYPES[@]}"; do
    for entrada in "${ENTRADAS[@]}"; do
        echo "=== type= $type | entrada=$entrada ==="

        for ((i=1; i<=REPETICOES; i++)); do
            echo "Execução $i/$REPETICOES"
            python3 main.py --type $type --open_text "decifras/$type-$entrada-$i.txt" --cipher_text "cifras/$type-$entrada-$i.txt" --key "keys/key-$type.txt" --cipher False
        done
    done
done


echo "Finalizado: 744 execuções."
