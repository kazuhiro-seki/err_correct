import os
import select

from fairseq.models.transformer import TransformerModel

IPC_FIFO_NAME_A = "pipe_a"
IPC_FIFO_NAME_B = "pipe_b"

# load model
model = TransformerModel.from_pretrained(
  './checkpoints/transformer_nag',
  checkpoint_file='checkpoint_best.pt',
  data_name_or_path='data-bin/transcript.tokenized.1m',
  bpe= 'subword_nmt',
  bpe_codes='examples/translation/transcript.tokenized/code'
)

def get_message(fifo):
    '''Read n bytes from pipe. Note: n=24 is an example'''
    return os.read(fifo, 128)

def process_msg(msg):
    '''Process message read from pipe'''
    return model.translate(msg)

if __name__ == "__main__":


    os.mkfifo(IPC_FIFO_NAME_A)  # Create Pipe A

    try:
        # pipe is opened as read only and in a non-blocking mode
        fifo_a = os.open(IPC_FIFO_NAME_A, os.O_RDONLY | os.O_NONBLOCK)  
        print('Pipe A ready')

        while True:
            try:
                fifo_b = os.open(IPC_FIFO_NAME_B, os.O_WRONLY)
                print("Pipe B ready")
                break
            except:
                # Wait until Pipe B has been initialized
                pass

        try:
            poll = select.poll()
            poll.register(fifo_a, select.POLLIN)

            try:
                while True:
                    # Poll every 1 sec
                    if (fifo_a, select.POLLIN) in poll.poll(1000):

                        # Read from Pipe A  
                        msg = get_message(fifo_a).decode("utf-8")
                        lines = msg.rstrip().split('\n')
                        for msg in lines:
                            print('----- Transcript from JS -----')
                            print("    " + msg)

                            # Process Message
                            msg = process_msg(msg)
                            print('----- Corrected -----')
                            print("    " + msg)

                            # Write to Pipe B
                            os.write(fifo_b, msg.encode("utf-8"))

            finally:
                poll.unregister(fifo_a)
        finally:
            os.close(fifo_a)
    finally:
        os.remove(IPC_FIFO_NAME_A)
        os.remove(IPC_FIFO_NAME_B)
