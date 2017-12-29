from src.processing import preprocess_image, postprocess_image
from src.relaxation_labelling import relax
import argparse
import cv2

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", help="input image", required=True)
    parser.add_argument("-o", "--output", help="output image", required=True)
    parser.add_argument("-v", "--visualize", help="visualize the output")
    parser.add_argument("-i", "--iterations", help="number of iterations",required=True)
    parser.add_argument("-s", "--shape", help="shape of the area",required=True)
    parser.add_argument('-c','--compatibility', nargs='+', help='<Required> Set flag', required=True)
    args = parser.parse_args()

    if len(args.compatibility)<4:
        raise Exception("Error: Compatibility coefficients incorrectly defined!")

    for i in range(4):
        args.compatibility[i] = float(args.compatibility[i])

    c = [[args.compatibility[0],args.compatibility[1]],
         [args.compatibility[2],args.compatibility[3]]]

    A,gray,edges = preprocess_image(args.data)

    A = relax(A, c, int(args.iterations), int(args.shape))

    A = postprocess_image(A)

    cv2.imwrite(str(args.output),A)

    if args.visualize == "1":
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax1 = fig.add_subplot(1,3,1)
        ax1.imshow(gray, cmap = 'gray', interpolation = 'bicubic')
        plt.xticks([])
        plt.yticks([])
        plt.title("Original grayscale image")
        ax2 = fig.add_subplot(1,3,2)
        ax2.imshow(edges, cmap = 'gray')
        plt.xticks([])
        plt.yticks([])
        plt.title("Edges")
        ax3 = fig.add_subplot(1,3,3)
        ax3.imshow(A, cmap = 'gray')
        plt.xticks([])
        plt.yticks([])
        plt.title("Refined edges")
        plt.show()
