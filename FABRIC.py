# nohup python FABRIC.py &
# nohup python FABRIC.py > /dev/null 2>&1 &
# nohup python FABRIC.py > output.log 2>&1 &

import FABRIC

def main():
  params = FABRIC.loadArgs('./params/params.yaml')
  FABRIC.genFabDf(params)

if __name__ == "__main__":
  main()