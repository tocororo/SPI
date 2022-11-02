import logging,os

def create_log(file_name):
    logger = logging
    file_name_path = f'temp/logs/{file_name}.log'
    os.makedirs(os.path.dirname(file_name_path), exist_ok=True)
    logger.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
                    datefmt='%I:%M:%S %p',
                    handlers=[
                        logging.FileHandler(file_name_path),
                        logging.StreamHandler()
                    ])
    return logger

if __name__ == '__main__':
    create_log('hello').warning('mensaje a nivel warning')
    # logging.info('mensaje a nivel info')
    # logging.debug('mensaje a nivel debug')
    # logging.error('Ocurrió un error en la base de datos')
    # logging.debug('se realizó la conexión con exito')