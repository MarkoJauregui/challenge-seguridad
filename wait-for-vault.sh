#!/bin/bash

# Espera a que Vault esté disponible
while ! curl -s http://vault:8200/v1/sys/health | grep -q '"initialized":true,"sealed":false'; do
  echo "Waiting for Vault to start..."
  sleep 2
done

echo "Vault is up and running!"
