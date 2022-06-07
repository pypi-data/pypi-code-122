from torch.utils.data import Dataset, DataLoader
import os
from PIL import Image
from torchvision.datasets.cifar import CIFAR10
from torchvision import transforms

def is_image_file(filename):
    IMG_EXTENSIONS = [
        '.jpg', '.JPG', '.jpeg', '.JPEG',
        '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP', '.tiff'
    ]
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)


def data_process(root, dataset, batch_size, device_ids, is_train=False, img_size=128):
    root = os.path.join(root, dataset)

    # train loader
    train_loader = None
    if dataset=='cifar10':
        normalize = transforms.Normalize(mean=[0.4914, 0.4822, 0.4465],
                                         std=[0.2023, 0.1994, 0.2010])
        train_transform = transforms.Compose([
            transforms.ToTensor(),
            normalize,
        ])
        test_transform = transforms.Compose([
            transforms.ToTensor(),
            normalize,
        ])
    else:
        train_transform = transforms.Compose([
            transforms.Resize((img_size, img_size), 0),
            #transforms.RandomCrop(img_size,4),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5],
                             std=[0.5, 0.5, 0.5])
        ])
        # test loader
        test_transform = transforms.Compose([
            transforms.Resize((img_size, img_size), 0),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5],
                                 std=[0.5, 0.5, 0.5])
        ])

    if is_train:
        if dataset == 'cifar10':
            train_dataset = CIFAR10(root, train=True, download=True, transform=train_transform)
        elif dataset == 'VOC_single':
            train_dataset = SingleDataset(root, train=True, transform=train_transform)
        else:
            train_dataset = CommonDataset(root, train=True, transform=train_transform)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True,
                                  num_workers=4 * len(device_ids), pin_memory=False)



    if dataset == 'cifar10':
        test_dataset = CIFAR10(root, train=False, download=True, transform=test_transform)
        num_classes = 10
    elif dataset =='VOC_single':
        test_dataset = SingleDataset(root, train=False, transform=test_transform)
        num_classes = test_dataset.num_classes
    else:
        test_dataset = CommonDataset(root, train=False, transform=test_transform)
        num_classes = test_dataset.num_classes
    test_loader = DataLoader(test_dataset, batch_size=batch_size,
                             num_workers=4 * len(device_ids), pin_memory=False)

    return train_loader, test_loader, num_classes

class CommonDataset(Dataset):
    def __init__(self, root, train=True, transform=None):
        self.paths = []
        self.labels = []
        self.transform = transform

        if train:
            data_dir = os.path.join(root, 'train')
        else:
            data_dir = os.path.join(root, 'test')

        self.num_classes = len(os.listdir(data_dir))
        print(data_dir)
        if ('animal' or 'NICO') in data_dir:
            for class_id, dirs in enumerate(os.listdir(data_dir)):
                class_dir = os.path.join(data_dir, dirs)
                for prop in os.listdir(class_dir):
                    property_dir = os.path.join(class_dir, prop)
                    for img in os.listdir(property_dir):
                        if not is_image_file(img):
                            continue
                        self.paths.append(os.path.join(class_dir, prop, img))
                        self.labels.append(class_id)
        else:
            for class_id, dirs in enumerate(os.listdir(data_dir)):
                class_dir = os.path.join(data_dir, dirs)
                if not os.path.isdir(class_dir):
                    continue
                for basename in os.listdir(class_dir):
                    if not is_image_file(basename):
                        continue
                    self.paths.append(os.path.join(class_dir, basename))
                    self.labels.append(class_id)


    def __len__(self):
        return len(self.paths)

    def __getitem__(self, item):
        path = self.paths[item]
        image = Image.open(path).convert('RGB')

        if self.transform:
            image = self.transform(image)
        label = self.labels[item]
        return image, label


class SingleDataset(Dataset):
    def __init__(self, root, train=True, transform=None):
        self.paths = []
        self.labels = []
        self.transform = transform

        if train:
            data_dir = os.path.join(root, 'train')
        else:
            data_dir = os.path.join(root, 'test')

        self.num_classes = len(os.listdir(data_dir))
        print(data_dir)
        for class_id, dirs in enumerate(os.listdir(data_dir)):
                class_dir = os.path.join(data_dir, dirs)
                if not os.path.isdir(class_dir):
                    continue
                for basename in os.listdir(class_dir):
                    if not is_image_file(basename):
                        continue
                    self.paths.append(os.path.join(class_dir, basename))
                    self.labels.append(class_id)


    def __len__(self):
        return len(self.paths)

    def __getitem__(self, item):
        path = self.paths[item]
        image = Image.open(path).convert('RGB')

        if self.transform:
            image = self.transform(image)
        label = self.labels[item]
        return image, label

class SegDataset(Dataset):
    def __init__(self, root, train=False, transform=None):
        self.paths = []
        self.labels = []
        self.seg_path=[]
        self.transform = transform

        if train:
            data_dir = os.path.join(root, 'train')
            seg_dir=None
            print('only for test, train maybe wrong')
        else:
            data_dir = os.path.join(root, 'test')
            seg_dir=os.path.join(root, 'segmentation')

        self.num_classes = len(os.listdir(data_dir))
        print(data_dir)
        for class_id, dirs in enumerate(os.listdir(data_dir)):
                class_dir = os.path.join(data_dir, dirs)
                seg_class=os.path.join(seg_dir,dirs)
                if not os.path.isdir(class_dir):
                    continue
                for basename in os.listdir(class_dir):
                    if not is_image_file(basename):
                        continue
                    self.paths.append(os.path.join(class_dir, basename))
                    basename2=os.path.splitext(basename)[0]+'.png'
                    self.seg_path.append(os.path.join(seg_class, basename2))
                    self.labels.append(class_id)


    def __len__(self):
        return len(self.paths)

    def __getitem__(self, item):
        path = self.paths[item]
        seg_path=self.seg_path[item]
        image = Image.open(path).convert('RGB')
        seg_img=Image.open(seg_path).convert('RGB')

        if self.transform:
            image = self.transform(image)
            seg_img=self.transform(seg_img)
        label = self.labels[item]
        return image,seg_img, label
