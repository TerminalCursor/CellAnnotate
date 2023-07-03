import tifffile

from Find_3D_annotation import Find_3D
## TEST CASE of two ellipsoids.
F = Find_3D()
#generate test mask with 2 ellipsoids that are overlapping, but oriented differently.
M, Mgt = F.generate_test_mask(nearby_xy = True, stacked = False, angled = False, overlapped = True)
#M is the ground truth Z-stack (H x W x Z). Mgt is the maximum projected version
# with one object in each channel (H x W x 2).
#Generate test image with noise.
IM = F.generate_test_image(M)
#compute 3D mask estimation from 2D max projections without providing a Z guess of cell locations.
_, Mtest = F.run_analysis(Mgt, IM)
#_, IMtest = F.run_analysis(Mgt, M)
#compute 3D mask estimation but this time provide guesses for cell Z slice locations.
_, Mbetter = F.run_analysis(Mgt, M, Zall = [5, 17])
#_, IMbetter = F.run_analysis(Mgt, IM, Zall = [5, 17])

#compare ground truth 3D mask and produced 3D estimated annotations.
#F.compare_z_stacks(M, Mbetter)
#often, pixels of Mbetter are missing due to the added noise in the generated image.
#compare image and 3D estimated annotations.
#F.compare_z_stacks(M, Mbetter)

F.save_zstack(IM, 'temp.ome.tif')


##With CellDataset
# CP = CellDataset(dataset_path="/Users/czeddy/Documents/Auto_Seg/CellAnnotate/CellAnnotate/datasets/example")
# CP.run_prep()
# M, IM, _ = CP.load_image_gt(0)
##import Find_3D_annotation
# F = Find_3D()
# O, Iall = F.run_analysis(M, IM)
# F.compare_z_stacks(np.squeeze(IM),Iall)

## With CellPose Network
# CP = CellPose(mode="training",dataset_path="/users/czeddy/documents/auto_seg/datasets/v7_mini",data_type="Cell3D")
# CP.import_train_val_data()
# mask = CP.dataset_train.load_mask(0)
# IM = CP.dataset_train.load_image(0, CP.config.INPUT_DIM, mask=mask)
##import Find_3D_annotation
# F = Find_3D()
# O, Iall = F.run_analysis(mask, IM)
# F.compare_z_stacks(np.squeeze(IM),Iall)
