# Memoria del Proyecto Universal History

## Contexto Actual
- Estamos trabajando en el proyecto `universal-history`, una biblioteca para crear, mantener y utilizar historiales universales a través de múltiples dominios.
- El proyecto está ubicado en: `/home/gabriel/Proyectos/empujon/universal-history`

## Estado Actual
1. **Estructura del Proyecto**:
   - `src/universal_history/` - Código fuente principal
     - `models/` - Modelos de datos (EventRecord, TrajectorySynthesis, etc.)
     - `services/` - Servicios principales (EventService, HistoryService, etc.)
     - `storage/` - Implementaciones de repositorios (memoria, MongoDB)
   - `tests/` - Pruebas organizadas por módulo

2. **Configuración**:
   - Entorno virtual creado en `.venv`
   - Dependencias instaladas con `pip install -e .[dev]`
   - Se está trabajando en el archivo `tests/models/test_event_record.py`

3. **Problemas Encontrados**:
   - Dificultades para ejecutar los tests (no se muestra salida)
   - Se intentó ejecutar con `python -m pytest` sin éxito visible

## Próximos Pasos
1. Solucionar problemas de ejecución de tests
2. Revisar la cobertura de pruebas
3. Asegurar que todas las funcionalidades críticas tengan pruebas adecuadas

## Comandos Útiles
```bash
# Activar entorno virtual
source .venv/bin/activate

# Instalar dependencias
pip install -e .[dev]

# Ejecutar tests (cuando se solucione el problema)
python -m pytest -v

# Ver cobertura de código
pytest --cov=universal_history
```

## Notas Adicionales
- El proyecto utiliza `pytest` para pruebas unitarias
- Hay una configuración de cobertura de código habilitada
- Se estaba trabajando específicamente en las pruebas del modelo `EventRecord`
