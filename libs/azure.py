import re
import time

import requests

import json


USER_DATA = """c3VkbyBzZWQgLWkuYmFrICcvXlNFTElOVVg9L2NTRUxJTlVYPWRpc2FibGVkJyAvZXRjL3N5c2NvbmZpZy9zZWxpbnV4OwpzdWRvIHNlZCAtaS5iYWsgJy9eU0VMSU5VWD0vY1NFTElOVVg9ZGlzYWJsZWQnIC9ldGMvc2VsaW51eC9jb25maWc7CnN1ZG8gc2V0ZW5mb3JjZSAwOwplY2hvIHJvb3Q6YWRtaW43Nzg4PT0gfHN1ZG8gY2hwYXNzd2Qgcm9vdApzdWRvIHNlZCAtaSAncy9eI1w/UGVybWl0Um9vdExvZ2luLiovUGVybWl0Um9vdExvZ2luIHllcy9nJyAvZXRjL3NzaC9zc2hkX2NvbmZpZzsKc3VkbyBzZWQgLWkgJ3MvXiNcP1Bhc3N3b3JkQXV0aGVudGljYXRpb24uKi9QYXNzd29yZEF1dGhlbnRpY2F0aW9uIHllcy9nJyAvZXRjL3NzaC9zc2hkX2NvbmZpZzsKc3VkbyBzZXJ2aWNlIHNzaGQgcmVzdGFydDsKc3VkbyBkZCBpZj0vZGV2L3plcm8gb2Y9L3Zhci9zd2FwIGJzPTEwMjQgY291bnQ9MjA0ODAwMDsKc3VkbyBta3N3YXAgL3Zhci9zd2FwOwpzdWRvIC9zYmluL3N3YXBvbiAvdmFyL3N3YXA7CnN1ZG8gZWNobyAiL3Zhci9zd2FwIHN3YXAgc3dhcCBkZWZhdWx0IDAgMCIgPj4gL2V0Yy9mc3RhYjs="""

VM_SIZES = {'Standard_B1ls': '1 vCPUs, 0.5 GB RAM', 'Standard_B1ms': '1 vCPUs, 2 GB RAM', 'Standard_B1s': '1 vCPUs, 1 GB RAM', 'Standard_B2ms': '2 vCPUs, 8 GB RAM', 'Standard_B2s': '2 vCPUs, 4 GB RAM', 'Standard_B4ms': '4 vCPUs, 16 GB RAM', 'Standard_B8ms': '8 vCPUs, 32 GB RAM', 'Standard_B12ms': '12 vCPUs, 48 GB RAM', 'Standard_B16ms': '16 vCPUs, 64 GB RAM', 'Standard_B20ms': '20 vCPUs, 80 GB RAM', 'Standard_DS1_v2': '1 vCPUs, 3.5 GB RAM', 'Standard_DS2_v2': '2 vCPUs, 7 GB RAM', 'Standard_DS3_v2': '4 vCPUs, 14 GB RAM', 'Standard_DS4_v2': '8 vCPUs, 28 GB RAM', 'Standard_DS5_v2': '16 vCPUs, 56 GB RAM', 'Standard_DS11-1_v2': '2 vCPUs, 14 GB RAM', 'Standard_DS11_v2': '2 vCPUs, 14 GB RAM', 'Standard_DS12-1_v2': '4 vCPUs, 28 GB RAM', 'Standard_DS12-2_v2': '4 vCPUs, 28 GB RAM', 'Standard_DS12_v2': '4 vCPUs, 28 GB RAM', 'Standard_DS13-2_v2': '8 vCPUs, 56 GB RAM', 'Standard_DS13-4_v2': '8 vCPUs, 56 GB RAM', 'Standard_DS13_v2': '8 vCPUs, 56 GB RAM', 'Standard_DS14-4_v2': '16 vCPUs, 112 GB RAM', 'Standard_DS14-8_v2': '16 vCPUs, 112 GB RAM', 'Standard_DS14_v2': '16 vCPUs, 112 GB RAM', 'Standard_DS15_v2': '20 vCPUs, 140 GB RAM', 'Standard_DS2_v2_Promo': '2 vCPUs, 7 GB RAM', 'Standard_DS3_v2_Promo': '4 vCPUs, 14 GB RAM', 'Standard_DS4_v2_Promo': '8 vCPUs, 28 GB RAM', 'Standard_DS5_v2_Promo': '16 vCPUs, 56 GB RAM', 'Standard_DS11_v2_Promo': '2 vCPUs, 14 GB RAM', 'Standard_DS12_v2_Promo': '4 vCPUs, 28 GB RAM', 'Standard_DS13_v2_Promo': '8 vCPUs, 56 GB RAM', 'Standard_DS14_v2_Promo': '16 vCPUs, 112 GB RAM', 'Standard_F1s': '1 vCPUs, 2 GB RAM', 'Standard_F2s': '2 vCPUs, 4 GB RAM', 'Standard_F4s': '4 vCPUs, 8 GB RAM', 'Standard_F8s': '8 vCPUs, 16 GB RAM', 'Standard_F16s': '16 vCPUs, 32 GB RAM', 'Standard_D2s_v3': '2 vCPUs, 8 GB RAM', 'Standard_D4s_v3': '4 vCPUs, 16 GB RAM', 'Standard_D8s_v3': '8 vCPUs, 32 GB RAM', 'Standard_D16s_v3': '16 vCPUs, 64 GB RAM', 'Standard_D32s_v3': '32 vCPUs, 128 GB RAM', 'Standard_A0': '1 vCPUs, 0.75 GB RAM', 'Standard_A1': '1 vCPUs, 1.75 GB RAM', 'Standard_A2': '2 vCPUs, 3.5 GB RAM', 'Standard_A3': '4 vCPUs, 7 GB RAM', 'Standard_A5': '2 vCPUs, 14 GB RAM', 'Standard_A4': '8 vCPUs, 14 GB RAM', 'Standard_A6': '4 vCPUs, 28 GB RAM', 'Standard_A7': '8 vCPUs, 56 GB RAM', 'Standard_D1_v2': '1 vCPUs, 3.5 GB RAM', 'Standard_D2_v2': '2 vCPUs, 7 GB RAM', 'Standard_D3_v2': '4 vCPUs, 14 GB RAM', 'Standard_D4_v2': '8 vCPUs, 28 GB RAM', 'Standard_D5_v2': '16 vCPUs, 56 GB RAM', 'Standard_D11_v2': '2 vCPUs, 14 GB RAM', 'Standard_D12_v2': '4 vCPUs, 28 GB RAM', 'Standard_D13_v2': '8 vCPUs, 56 GB RAM', 'Standard_D14_v2': '16 vCPUs, 112 GB RAM', 'Standard_D15_v2': '20 vCPUs, 140 GB RAM', 'Standard_D2_v2_Promo': '2 vCPUs, 7 GB RAM', 'Standard_D3_v2_Promo': '4 vCPUs, 14 GB RAM', 'Standard_D4_v2_Promo': '8 vCPUs, 28 GB RAM', 'Standard_D5_v2_Promo': '16 vCPUs, 56 GB RAM', 'Standard_D11_v2_Promo': '2 vCPUs, 14 GB RAM', 'Standard_D12_v2_Promo': '4 vCPUs, 28 GB RAM', 'Standard_D13_v2_Promo': '8 vCPUs, 56 GB RAM', 'Standard_D14_v2_Promo': '16 vCPUs, 112 GB RAM', 'Standard_F1': '1 vCPUs, 2 GB RAM', 'Standard_F2': '2 vCPUs, 4 GB RAM', 'Standard_F4': '4 vCPUs, 8 GB RAM', 'Standard_F8': '8 vCPUs, 16 GB RAM', 'Standard_F16': '16 vCPUs, 32 GB RAM', 'Standard_A1_v2': '1 vCPUs, 2 GB RAM', 'Standard_A2m_v2': '2 vCPUs, 16 GB RAM', 'Standard_A2_v2': '2 vCPUs, 4 GB RAM', 'Standard_A4m_v2': '4 vCPUs, 32 GB RAM', 'Standard_A4_v2': '4 vCPUs, 8 GB RAM', 'Standard_A8m_v2': '8 vCPUs, 64 GB RAM', 'Standard_A8_v2': '8 vCPUs, 16 GB RAM', 'Standard_NC4as_T4_v3': '4 vCPUs, 28 GB RAM', 'Standard_NC8as_T4_v3': '8 vCPUs, 56 GB RAM', 'Standard_NC16as_T4_v3': '16 vCPUs, 110 GB RAM', 'Standard_NC64as_T4_v3': '64 vCPUs, 440 GB RAM', 'Standard_E2_v4': '2 vCPUs, 16 GB RAM', 'Standard_E4_v4': '4 vCPUs, 32 GB RAM', 'Standard_E8_v4': '8 vCPUs, 64 GB RAM', 'Standard_E16_v4': '16 vCPUs, 128 GB RAM', 'Standard_E20_v4': '20 vCPUs, 160 GB RAM', 'Standard_E32_v4': '32 vCPUs, 256 GB RAM', 'Standard_E48_v4': '48 vCPUs, 384 GB RAM', 'Standard_E64_v4': '64 vCPUs, 504 GB RAM', 'Standard_E2d_v4': '2 vCPUs, 16 GB RAM', 'Standard_E4d_v4': '4 vCPUs, 32 GB RAM', 'Standard_E8d_v4': '8 vCPUs, 64 GB RAM', 'Standard_E16d_v4': '16 vCPUs, 128 GB RAM', 'Standard_E20d_v4': '20 vCPUs, 160 GB RAM', 'Standard_E32d_v4': '32 vCPUs, 256 GB RAM', 'Standard_E48d_v4': '48 vCPUs, 384 GB RAM', 'Standard_E64d_v4': '64 vCPUs, 504 GB RAM', 'Standard_E2s_v4': '2 vCPUs, 16 GB RAM', 'Standard_E4-2s_v4': '4 vCPUs, 32 GB RAM', 'Standard_E4s_v4': '4 vCPUs, 32 GB RAM', 'Standard_E8-2s_v4': '8 vCPUs, 64 GB RAM', 'Standard_E8-4s_v4': '8 vCPUs, 64 GB RAM', 'Standard_E8s_v4': '8 vCPUs, 64 GB RAM', 'Standard_E16-4s_v4': '16 vCPUs, 128 GB RAM', 'Standard_E16-8s_v4': '16 vCPUs, 128 GB RAM', 'Standard_E16s_v4': '16 vCPUs, 128 GB RAM', 'Standard_E20s_v4': '20 vCPUs, 160 GB RAM', 'Standard_E32-8s_v4': '32 vCPUs, 256 GB RAM', 'Standard_E32-16s_v4': '32 vCPUs, 256 GB RAM', 'Standard_E32s_v4': '32 vCPUs, 256 GB RAM', 'Standard_E48s_v4': '48 vCPUs, 384 GB RAM', 'Standard_E64-16s_v4': '64 vCPUs, 504 GB RAM', 'Standard_E64-32s_v4': '64 vCPUs, 504 GB RAM', 'Standard_E64s_v4': '64 vCPUs, 504 GB RAM', 'Standard_E80is_v4': '80 vCPUs, 504 GB RAM', 'Standard_E2ds_v4': '2 vCPUs, 16 GB RAM', 'Standard_E4-2ds_v4': '4 vCPUs, 32 GB RAM', 'Standard_E4ds_v4': '4 vCPUs, 32 GB RAM', 'Standard_E8-2ds_v4': '8 vCPUs, 64 GB RAM', 'Standard_E8-4ds_v4': '8 vCPUs, 64 GB RAM', 'Standard_E8ds_v4': '8 vCPUs, 64 GB RAM', 'Standard_E16-4ds_v4': '16 vCPUs, 128 GB RAM', 'Standard_E16-8ds_v4': '16 vCPUs, 128 GB RAM', 'Standard_E16ds_v4': '16 vCPUs, 128 GB RAM', 'Standard_E20ds_v4': '20 vCPUs, 160 GB RAM', 'Standard_E32-8ds_v4': '32 vCPUs, 256 GB RAM', 'Standard_E32-16ds_v4': '32 vCPUs, 256 GB RAM', 'Standard_E32ds_v4': '32 vCPUs, 256 GB RAM', 'Standard_E48ds_v4': '48 vCPUs, 384 GB RAM', 'Standard_E64-16ds_v4': '64 vCPUs, 504 GB RAM', 'Standard_E64-32ds_v4': '64 vCPUs, 504 GB RAM', 'Standard_E64ds_v4': '64 vCPUs, 504 GB RAM', 'Standard_E80ids_v4': '80 vCPUs, 504 GB RAM', 'Standard_D2d_v4': '2 vCPUs, 8 GB RAM', 'Standard_D4d_v4': '4 vCPUs, 16 GB RAM', 'Standard_D8d_v4': '8 vCPUs, 32 GB RAM', 'Standard_D16d_v4': '16 vCPUs, 64 GB RAM', 'Standard_D32d_v4': '32 vCPUs, 128 GB RAM', 'Standard_D48d_v4': '48 vCPUs, 192 GB RAM', 'Standard_D64d_v4': '64 vCPUs, 256 GB RAM', 'Standard_D2_v4': '2 vCPUs, 8 GB RAM', 'Standard_D4_v4': '4 vCPUs, 16 GB RAM', 'Standard_D8_v4': '8 vCPUs, 32 GB RAM', 'Standard_D16_v4': '16 vCPUs, 64 GB RAM', 'Standard_D32_v4': '32 vCPUs, 128 GB RAM', 'Standard_D48_v4': '48 vCPUs, 192 GB RAM', 'Standard_D64_v4': '64 vCPUs, 256 GB RAM', 'Standard_D2ds_v4': '2 vCPUs, 8 GB RAM', 'Standard_D4ds_v4': '4 vCPUs, 16 GB RAM', 'Standard_D8ds_v4': '8 vCPUs, 32 GB RAM', 'Standard_D16ds_v4': '16 vCPUs, 64 GB RAM', 'Standard_D32ds_v4': '32 vCPUs, 128 GB RAM', 'Standard_D48ds_v4': '48 vCPUs, 192 GB RAM', 'Standard_D64ds_v4': '64 vCPUs, 256 GB RAM', 'Standard_D2s_v4': '2 vCPUs, 8 GB RAM', 'Standard_D4s_v4': '4 vCPUs, 16 GB RAM', 'Standard_D8s_v4': '8 vCPUs, 32 GB RAM', 'Standard_D16s_v4': '16 vCPUs, 64 GB RAM', 'Standard_D32s_v4': '32 vCPUs, 128 GB RAM', 'Standard_D48s_v4': '48 vCPUs, 192 GB RAM', 'Standard_D64s_v4': '64 vCPUs, 256 GB RAM', 'Standard_D2_v3': '2 vCPUs, 8 GB RAM', 'Standard_D4_v3': '4 vCPUs, 16 GB RAM', 'Standard_D8_v3': '8 vCPUs, 32 GB RAM', 'Standard_D16_v3': '16 vCPUs, 64 GB RAM', 'Standard_D32_v3': '32 vCPUs, 128 GB RAM', 'Standard_D48_v3': '48 vCPUs, 192 GB RAM', 'Standard_D64_v3': '64 vCPUs, 256 GB RAM', 'Standard_D48s_v3': '48 vCPUs, 192 GB RAM', 'Standard_D64s_v3': '64 vCPUs, 256 GB RAM', 'Standard_E2_v3': '2 vCPUs, 16 GB RAM', 'Standard_E4_v3': '4 vCPUs, 32 GB RAM', 'Standard_E8_v3': '8 vCPUs, 64 GB RAM', 'Standard_E16_v3': '16 vCPUs, 128 GB RAM', 'Standard_E20_v3': '20 vCPUs, 160 GB RAM', 'Standard_E32_v3': '32 vCPUs, 256 GB RAM', 'Standard_E48_v3': '48 vCPUs, 384 GB RAM', 'Standard_E64_v3': '64 vCPUs, 432 GB RAM', 'Standard_E2s_v3': '2 vCPUs, 16 GB RAM', 'Standard_E4-2s_v3': '4 vCPUs, 32 GB RAM', 'Standard_E4s_v3': '4 vCPUs, 32 GB RAM', 'Standard_E8-2s_v3': '8 vCPUs, 64 GB RAM', 'Standard_E8-4s_v3': '8 vCPUs, 64 GB RAM', 'Standard_E8s_v3': '8 vCPUs, 64 GB RAM', 'Standard_E16-4s_v3': '16 vCPUs, 128 GB RAM', 'Standard_E16-8s_v3': '16 vCPUs, 128 GB RAM', 'Standard_E16s_v3': '16 vCPUs, 128 GB RAM', 'Standard_E20s_v3': '20 vCPUs, 160 GB RAM', 'Standard_E32-8s_v3': '32 vCPUs, 256 GB RAM', 'Standard_E32-16s_v3': '32 vCPUs, 256 GB RAM', 'Standard_E32s_v3': '32 vCPUs, 256 GB RAM', 'Standard_E48s_v3': '48 vCPUs, 384 GB RAM', 'Standard_E64-16s_v3': '64 vCPUs, 432 GB RAM', 'Standard_E64-32s_v3': '64 vCPUs, 432 GB RAM', 'Standard_E64s_v3': '64 vCPUs, 432 GB RAM', 'Standard_F2s_v2': '2 vCPUs, 4 GB RAM', 'Standard_F4s_v2': '4 vCPUs, 8 GB RAM', 'Standard_F8s_v2': '8 vCPUs, 16 GB RAM', 'Standard_F16s_v2': '16 vCPUs, 32 GB RAM', 'Standard_F32s_v2': '32 vCPUs, 64 GB RAM', 'Standard_F48s_v2': '48 vCPUs, 96 GB RAM', 'Standard_F64s_v2': '64 vCPUs, 128 GB RAM', 'Standard_F72s_v2': '72 vCPUs, 144 GB RAM', 'Standard_E64i_v3': '64 vCPUs, 432 GB RAM', 'Standard_E64is_v3': '64 vCPUs, 432 GB RAM', 'Standard_D1': '1 vCPUs, 3.5 GB RAM', 'Standard_D2': '2 vCPUs, 7 GB RAM', 'Standard_D3': '4 vCPUs, 14 GB RAM', 'Standard_D4': '8 vCPUs, 28 GB RAM', 'Standard_D11': '2 vCPUs, 14 GB RAM', 'Standard_D12': '4 vCPUs, 28 GB RAM', 'Standard_D13': '8 vCPUs, 56 GB RAM', 'Standard_D14': '16 vCPUs, 112 GB RAM', 'Standard_DS1': '1 vCPUs, 3.5 GB RAM', 'Standard_DS2': '2 vCPUs, 7 GB RAM', 'Standard_DS3': '4 vCPUs, 14 GB RAM', 'Standard_DS4': '8 vCPUs, 28 GB RAM', 'Standard_DS11': '2 vCPUs, 14 GB RAM', 'Standard_DS12': '4 vCPUs, 28 GB RAM', 'Standard_DS13': '8 vCPUs, 56 GB RAM', 'Standard_DS14': '16 vCPUs, 112 GB RAM', 'Standard_DC8_v2': '8 vCPUs, 32 GB RAM', 'Standard_DC1s_v2': '1 vCPUs, 4 GB RAM', 'Standard_DC2s_v2': '2 vCPUs, 8 GB RAM', 'Standard_DC4s_v2': '4 vCPUs, 16 GB RAM', 'Standard_L8s_v2': '8 vCPUs, 64 GB RAM', 'Standard_L16s_v2': '16 vCPUs, 128 GB RAM', 'Standard_L32s_v2': '32 vCPUs, 256 GB RAM', 'Standard_L48s_v2': '48 vCPUs, 384 GB RAM', 'Standard_L64s_v2': '64 vCPUs, 512 GB RAM', 'Standard_L80s_v2': '80 vCPUs, 640 GB RAM', 'Standard_NV4as_v4': '4 vCPUs, 14 GB RAM', 'Standard_NV8as_v4': '8 vCPUs, 28 GB RAM', 'Standard_NV16as_v4': '16 vCPUs, 56 GB RAM', 'Standard_NV32as_v4': '32 vCPUs, 112 GB RAM', 'Standard_G1': '2 vCPUs, 28 GB RAM', 'Standard_G2': '4 vCPUs, 56 GB RAM', 'Standard_G3': '8 vCPUs, 112 GB RAM', 'Standard_G4': '16 vCPUs, 224 GB RAM', 'Standard_G5': '32 vCPUs, 448 GB RAM', 'Standard_GS1': '2 vCPUs, 28 GB RAM', 'Standard_GS2': '4 vCPUs, 56 GB RAM', 'Standard_GS3': '8 vCPUs, 112 GB RAM', 'Standard_GS4': '16 vCPUs, 224 GB RAM', 'Standard_GS4-4': '16 vCPUs, 224 GB RAM', 'Standard_GS4-8': '16 vCPUs, 224 GB RAM', 'Standard_GS5': '32 vCPUs, 448 GB RAM', 'Standard_GS5-8': '32 vCPUs, 448 GB RAM', 'Standard_GS5-16': '32 vCPUs, 448 GB RAM', 'Standard_L4s': '4 vCPUs, 32 GB RAM', 'Standard_L8s': '8 vCPUs, 64 GB RAM', 'Standard_L16s': '16 vCPUs, 128 GB RAM', 'Standard_L32s': '32 vCPUs, 256 GB RAM', 'Standard_NC6s_v3': '6 vCPUs, 112 GB RAM', 'Standard_NC12s_v3': '12 vCPUs, 224 GB RAM', 'Standard_NC24rs_v3': '24 vCPUs, 448 GB RAM', 'Standard_NC24s_v3': '24 vCPUs, 448 GB RAM', 'Standard_M64': '64 vCPUs, 1000 GB RAM', 'Standard_M64m': '64 vCPUs, 1750 GB RAM', 'Standard_M128': '128 vCPUs, 2000 GB RAM', 'Standard_M128m': '128 vCPUs, 3800 GB RAM', 'Standard_M8-2ms': '8 vCPUs, 218.75 GB RAM', 'Standard_M8-4ms': '8 vCPUs, 218.75 GB RAM', 'Standard_M8ms': '8 vCPUs, 218.75 GB RAM', 'Standard_M16-4ms': '16 vCPUs, 437.5 GB RAM', 'Standard_M16-8ms': '16 vCPUs, 437.5 GB RAM', 'Standard_M16ms': '16 vCPUs, 437.5 GB RAM', 'Standard_M32-8ms': '32 vCPUs, 875 GB RAM', 'Standard_M32-16ms': '32 vCPUs, 875 GB RAM', 'Standard_M32ls': '32 vCPUs, 256 GB RAM', 'Standard_M32ms': '32 vCPUs, 875 GB RAM', 'Standard_M32ts': '32 vCPUs, 192 GB RAM', 'Standard_M64-16ms': '64 vCPUs, 1750 GB RAM', 'Standard_M64-32ms': '64 vCPUs, 1750 GB RAM', 'Standard_M64ls': '64 vCPUs, 512 GB RAM', 'Standard_M64ms': '64 vCPUs, 1750 GB RAM', 'Standard_M64s': '64 vCPUs, 1000 GB RAM', 'Standard_M128-32ms': '128 vCPUs, 3800 GB RAM', 'Standard_M128-64ms': '128 vCPUs, 3800 GB RAM', 'Standard_M128ms': '128 vCPUs, 3800 GB RAM', 'Standard_M128s': '128 vCPUs, 2000 GB RAM', 'Standard_M32ms_v2': '32 vCPUs, 875 GB RAM', 'Standard_M64ms_v2': '64 vCPUs, 1792 GB RAM', 'Standard_M64s_v2': '64 vCPUs, 1024 GB RAM', 'Standard_M128ms_v2': '128 vCPUs, 3892 GB RAM', 'Standard_M128s_v2': '128 vCPUs, 2048 GB RAM', 'Standard_M192ims_v2': '192 vCPUs, 4096 GB RAM', 'Standard_M192is_v2': '192 vCPUs, 2048 GB RAM', 'Standard_M32dms_v2': '32 vCPUs, 875 GB RAM', 'Standard_M64dms_v2': '64 vCPUs, 1792 GB RAM', 'Standard_M64ds_v2': '64 vCPUs, 1024 GB RAM', 'Standard_M128dms_v2': '128 vCPUs, 3892 GB RAM', 'Standard_M128ds_v2': '128 vCPUs, 2048 GB RAM', 'Standard_M192idms_v2': '192 vCPUs, 4096 GB RAM', 'Standard_M192ids_v2': '192 vCPUs, 2048 GB RAM', 'Standard_NV6s_v2': '6 vCPUs, 112 GB RAM', 'Standard_NV12s_v2': '12 vCPUs, 224 GB RAM', 'Standard_NV24s_v2': '24 vCPUs, 448 GB RAM', 'Standard_NV12s_v3': '12 vCPUs, 112 GB RAM', 'Standard_NV24s_v3': '24 vCPUs, 224 GB RAM', 'Standard_NV48s_v3': '48 vCPUs, 448 GB RAM', 'Standard_H8': '8 vCPUs, 56 GB RAM', 'Standard_H8_Promo': '8 vCPUs, 56 GB RAM', 'Standard_H16': '16 vCPUs, 112 GB RAM', 'Standard_H16_Promo': '16 vCPUs, 112 GB RAM', 'Standard_H8m': '8 vCPUs, 112 GB RAM', 'Standard_H8m_Promo': '8 vCPUs, 112 GB RAM', 'Standard_H16m': '16 vCPUs, 224 GB RAM', 'Standard_H16m_Promo': '16 vCPUs, 224 GB RAM', 'Standard_H16r': '16 vCPUs, 112 GB RAM', 'Standard_H16r_Promo': '16 vCPUs, 112 GB RAM', 'Standard_H16mr': '16 vCPUs, 224 GB RAM', 'Standard_H16mr_Promo': '16 vCPUs, 224 GB RAM', 'Standard_D2a_v4': '2 vCPUs, 8 GB RAM', 'Standard_D4a_v4': '4 vCPUs, 16 GB RAM', 'Standard_D8a_v4': '8 vCPUs, 32 GB RAM', 'Standard_D16a_v4': '16 vCPUs, 64 GB RAM', 'Standard_D32a_v4': '32 vCPUs, 128 GB RAM', 'Standard_D48a_v4': '48 vCPUs, 192 GB RAM', 'Standard_D64a_v4': '64 vCPUs, 256 GB RAM', 'Standard_D96a_v4': '96 vCPUs, 384 GB RAM', 'Standard_D2as_v4': '2 vCPUs, 8 GB RAM', 'Standard_D4as_v4': '4 vCPUs, 16 GB RAM', 'Standard_D8as_v4': '8 vCPUs, 32 GB RAM', 'Standard_D16as_v4': '16 vCPUs, 64 GB RAM', 'Standard_D32as_v4': '32 vCPUs, 128 GB RAM', 'Standard_D48as_v4': '48 vCPUs, 192 GB RAM', 'Standard_D64as_v4': '64 vCPUs, 256 GB RAM', 'Standard_D96as_v4': '96 vCPUs, 384 GB RAM', 'Standard_E2a_v4': '2 vCPUs, 16 GB RAM', 'Standard_E4a_v4': '4 vCPUs, 32 GB RAM', 'Standard_E8a_v4': '8 vCPUs, 64 GB RAM', 'Standard_E16a_v4': '16 vCPUs, 128 GB RAM', 'Standard_E20a_v4': '20 vCPUs, 160 GB RAM', 'Standard_E32a_v4': '32 vCPUs, 256 GB RAM', 'Standard_E48a_v4': '48 vCPUs, 384 GB RAM', 'Standard_E64a_v4': '64 vCPUs, 512 GB RAM', 'Standard_E96a_v4': '96 vCPUs, 672 GB RAM', 'Standard_E2as_v4': '2 vCPUs, 16 GB RAM', 'Standard_E4-2as_v4': '4 vCPUs, 32 GB RAM', 'Standard_E4as_v4': '4 vCPUs, 32 GB RAM', 'Standard_E8-2as_v4': '8 vCPUs, 64 GB RAM', 'Standard_E8-4as_v4': '8 vCPUs, 64 GB RAM', 'Standard_E8as_v4': '8 vCPUs, 64 GB RAM', 'Standard_E16-4as_v4': '16 vCPUs, 128 GB RAM', 'Standard_E16-8as_v4': '16 vCPUs, 128 GB RAM', 'Standard_E16as_v4': '16 vCPUs, 128 GB RAM', 'Standard_E20as_v4': '20 vCPUs, 160 GB RAM', 'Standard_E32-8as_v4': '32 vCPUs, 256 GB RAM', 'Standard_E32-16as_v4': '32 vCPUs, 256 GB RAM', 'Standard_E32as_v4': '32 vCPUs, 256 GB RAM', 'Standard_E48as_v4': '48 vCPUs, 384 GB RAM', 'Standard_E64-16as_v4': '64 vCPUs, 512 GB RAM', 'Standard_E64-32as_v4': '64 vCPUs, 512 GB RAM', 'Standard_E64as_v4': '64 vCPUs, 512 GB RAM', 'Standard_E96-24as_v4': '96 vCPUs, 672 GB RAM', 'Standard_E96-48as_v4': '96 vCPUs, 672 GB RAM', 'Standard_E96as_v4': '96 vCPUs, 672 GB RAM', 'Standard_M208ms_v2': '208 vCPUs, 5700 GB RAM', 'Standard_M208s_v2': '208 vCPUs, 2850 GB RAM', 'Standard_M416-208s_v2': '416 vCPUs, 5700 GB RAM', 'Standard_M416s_v2': '416 vCPUs, 5700 GB RAM', 'Standard_M416-208ms_v2': '416 vCPUs, 11400 GB RAM', 'Standard_M416ms_v2': '416 vCPUs, 11400 GB RAM'}


class AzureApi():

    def __init__(self, client_id, client_secret, tenant):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant = tenant
        self.subscriptionId = ''
        self.group_name = 'AzureGroup'

        self.access_token = ''
        self.curl = requests.session()
        self.curl.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

    # 获取最新token
    def get_token(self, token=''):
        try:
            if token in '':
                url = f'https://login.microsoftonline.com/{self.tenant}/oauth2/token'
                data = {
                    'grant_type': 'client_credentials',
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'resource': 'https://management.azure.com/',
                }
                ret = self.curl.post(url, data=data)
                self.access_token = ret.json()['access_token']

            else:
                self.access_token = token
            self.curl.headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            return True
        except:
            return False

    # 获取订阅详情
    def get_subscriptions(self):
        try:
            url = 'https://management.azure.com/subscriptions?api-version=2020-01-01'
            if not self.report_get(url):
                return False
            # print(self.result)
            self.subscriptionId = self.result['value'][0]['subscriptionId']
            self.display_name = self.result['value'][0]['displayName']
            self.status = self.result['value'][0]['state']
            return True
        except:
            return False
        # print(self.result)

    # 获取全部vm实例
    def get_vm_list(self, group_name='AzureGroup'):
        self.vm_list = []
        try:
            url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/providers/Microsoft.Compute/virtualMachines?api-version=2021-03-01'
            self.report_get(url)
            for vm in self.result['value']:
                try:
                    name = vm['name']
                    vm_id = vm['properties']['vmId']
                    location = vm['location']
                    group = re.findall(r'resourceGroups\/(.*)\/providers', vm['id'])[0]
                    vm_size = vm['properties']['hardwareProfile']['vmSize']

                    image = [
                        vm['properties']['storageProfile']['imageReference']['publisher'],
                        vm['properties']['storageProfile']['imageReference']['offer'],
                        vm['properties']['storageProfile']['imageReference']['sku'],
                        vm['properties']['storageProfile']['imageReference']['version']
                    ]

                    nic_name = vm['properties']['networkProfile']['networkInterfaces'][0]['id'].split('/')[-1]
                    image = ':'.join(image)
                    os_disk = vm['properties']['storageProfile']['osDisk'].get('diskSizeGB', 0)
                    _data = {
                        'name': name,
                        'vm_id': vm_id,
                        'location': location,
                        'group': group,
                        'vm_size': vm_size,
                        'os_disk': os_disk,
                        'nic_name': nic_name,
                        'image': image
                    }
                    self.vm_list.append(_data)
                except:
                    continue
            return True
        except BaseException as e:
            print(e)
            return False

    # 获取 vm 实例信息
    def get_vm_info(self, vm_name):
        try:
            url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Compute/virtualMachines/{vm_name}/instanceView?api-version=2021-03-01'
            self.report_get(url)
            self.status = self.result['statuses'][1]['displayStatus']
            return True
        except BaseException as e:
            print("获取vm 失败", e)
            return False

    # 通过公网IP名称获取公网IP信息
    def get_public_ip_info(self, public_ip_name):
        try:
            url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Network/publicIPAddresses/{public_ip_name}/?api-version=2020-11-01'
            if not self.report_get(url): return False

            self.public_ip = self.result['properties']['ipAddress']
            return True
        except:
            self.public_ip = ''
            return False

    # 查询 网络接口信息
    def get_network_nic(self, nic_name):
        try:
            url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Network/networkInterfaces/{nic_name}?api-version=2020-11-01'
            self.report_get(url)
            self.nic_info = self.result
            self.public_ip_name = self.result['properties']['ipConfigurations'][0]['properties']['publicIPAddress']['id'].split('/')[-1]
            return True
        except:
            return False

    # 订阅重命名
    def subscriptions_rename(self, name):
        url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/providers/Microsoft.Subscription/rename?api-version=2020-09-01'
        data = {
            'subscriptionName': name
        }
        self.curl.post(url, data=data, timeout=30)

    # vm 电源操作
    def vm_poer_action(self, vm_name, action):
        try:
            url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Compute/virtualMachines/{vm_name}/{action}?api-version=2021-03-01'
            ret = self.curl.post(url, timeout=30)
            if ret.status_code in [200, 202]:
                return True
            return False
        except:
            return False

    # 删除 VM 实例
    def vm_delete(self, vm_name):
        url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Compute/virtualMachines/{vm_name}?api-version=2021-03-01'
        ret = self.curl.delete(url, timeout=30)
        if ret.status_code in [200, 202]:

            _name = f'{vm_name}_disk'
            for num in range(10):
                if self.vm_disk_delete(_name):
                    print(f'{_name} 删除成功')
                    break
                print(f'第 {num} 次删除 {_name} 口失败, 等待3秒之后重新操作')
                time.sleep(5)
                continue
            else:
                print(f'删除 {_name} 失败')
            for num in range(10):
                if self.network_nic_delete(f'{vm_name}_nic'):
                    print(f'{vm_name}_nic 网络接口删除成功')
                    break
                print(f'第 {num} 次删除 {vm_name}_nic 网络接口失败, 等待3秒之后重新操作')
                time.sleep(5)
                continue
            else:
                print('删除网络接口失败')

            for num in range(10):
                if self.network_public_ip_delete(f'{vm_name}_public_ip'):
                    print(f'{vm_name}_public_ip 公共IP 删除成功')
                    break
                print(f'第 {num} 次删除 {vm_name}_public_ip 公共IP失败, 等待3秒之后重新操作')
                time.sleep(3)
                continue
            else:
                print('删除公共IP失败')
            return True
        return False

    # 删除 硬盘
    def vm_disk_delete(self, name):
        url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Compute/disks/{name}?api-version=2020-12-01'
        # print(url)
        ret = self.curl.delete(url, timeout=30)
        # print(ret.status_code)
        # print(ret.text)
        if ret.status_code in [200, 202]: return True
        return False

    # 删除 网络接口
    def network_nic_delete(self, name):
        url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Network/networkInterfaces/{name}?api-version=2020-11-01'
        ret = self.curl.delete(url, timeout=30)
        if ret.status_code in [200, 202]: return True
        return False

    # 删除 公网IP
    def network_public_ip_delete(self, name):
        url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Network/publicIPAddresses/{name}?api-version=2020-11-01'
        ret = self.curl.delete(url, timeout=30)
        if ret.status_code in [200, 202]: return True
        return False

    # 创建资源组
    def create_group(self):
        try:
            url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourcegroups/{self.group_name}?api-version=2021-04-01'
            data = {
                'location': 'eastus'
            }
            self.report_put_json(url, data)
            if self.result['location'] == 'eastus': return True
            return False
        except BaseException as e:
            print(e)
            return False

    # 创建虚拟网络, 传参 资源组名称, 虚拟网络名称
    def create_virtual_networks(self, vnet_name='AzureVnet', location='eastus'):
        url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Network/virtualNetworks/{vnet_name.lower()}_{location}?api-version=2020-11-01'
        self.report_get(url)
        self.vnet_name = self.result.get('name', False)
        if self.vnet_name == f'{vnet_name.lower()}_{location}':
            print(f'{vnet_name.lower()}_{location} 虚拟网络已存在')
            return True
        print(self.result)

        try:
            url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Network/virtualNetworks/{vnet_name.lower()}_{location}?api-version=2020-11-01'
            data = {
                'location': location,
                'properties': {
                    'addressSpace': {
                        'addressPrefixes': ['10.0.0.0/16']
                    }
                }
            }
            self.report_put_json(url, data)
            print(self.result)
            if self.result['location'] == location:
                self.vnet_name = self.result['name']
                return True
            return False
        except BaseException as e:
            print(e)
            return False

    # 创建公网IP
    def create_public_ip(self, public_ip_name='cdntip', location='eastus'):
        try:
            url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Network/publicIPAddresses/{public_ip_name}_public_ip?api-version=2020-11-01'
            data = {
                "properties": {
                    "publicIPAllocationMethod": "Dynamic",
                    "idleTimeoutInMinutes": 4,
                    "publicIPAddressVersion": "IPv4"
                },
                "sku": {
                    "name": "Basic",
                    "tier": "Regional"
                },
                "location": location
            }
            self.report_put_json(url, data)
            self.public_ip_name = self.result['name']
            self.public_ip_id = self.result['id']
            return True
        except:
            return False

    # 创建 虚拟网络 子网
    def create_subnet(self, vnet_name='AzureVneteastasia', sub_name='cdntip'):
        # 需要先查询子网是否存在
        url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Network/virtualNetworks/{vnet_name}/subnets/{sub_name}_subnet?api-version=2020-11-01'

        if not self.report_get(url): return False

        self.sub_id = self.result.get('id', False)
        self.sub_name = self.result.get('name', False)
        if self.sub_name == sub_name: return True

        try:
            url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Network/virtualNetworks/{vnet_name}/subnets/{sub_name}_subnet?api-version=2020-11-01'
            data = {
                'properties': {
                    'addressPrefix': '10.0.0.0/24'
                }
            }
            self.report_put_json(url, data)
            self.sub_id = self.result['id']
            self.sub_name = self.result['name']
            return True
        except BaseException as e:
            print(e)
            return False

    # 创建网络接口
    def create_nic(self, location='eastus', nic_name='cdntip', public_ip_id=None, subnet_id=''):
        try:
            url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Network/networkInterfaces/{nic_name}_nic?api-version=2020-11-01'
            data = {
                "properties": {
                    "enableAcceleratedNetworking": False,
                    "ipConfigurations": [
                        {
                            "name": "ipconfig1",
                            "properties": {
                                "publicIPAddress": {
                                    "id": public_ip_id
                                },
                                "subnet": {
                                    "id": subnet_id
                                }
                            }
                        }
                    ]
                },
                "location": location
            }
            self.report_put_json(url, data)
            self.nic_id = self.result['id']
            self.nic_name = self.result['name']
            return True
        except:
            return False

    # 重置网络接口  换IP
    def reset_nic(self, nic_name='cdntip'):


        try:
            # 1. 先查询网络接口信息
            url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Network/networkInterfaces/{nic_name}?api-version=2020-11-01'
            self.report_get(url)
            # print(url)
            subnet_id = self.result['properties']['ipConfigurations'][0]['properties']['subnet']['id']
            try:
                public_id = self.result['properties']['ipConfigurations'][0]['properties']['publicIPAddress']['id']
            except:
                public_id = f'/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Network/publicIPAddresses/{nic_name}_public_ip'
            location = self.result['location']

            data = {
                "properties": {
                    "enableAcceleratedNetworking": False,
                    "ipConfigurations": [
                        {
                            "name": "ipconfig1",
                            "properties": {
                                "publicIPAddress": None,
                                "subnet": {
                                    "id": subnet_id
                                }
                            }
                        }
                    ]
                },
                "location": location
            }
            # print(data)
            self.report_put_json(url, data)
            # print(self.result)
            data['properties']['ipConfigurations'][0]['properties']['publicIPAddress'] = {
                'id': public_id
            }

            for num in range(20):
                self.report_put_json(url, data)
                if self.result.get('error', 'sss') in ['sss']: break
                print(f'第 {num} 次, 网络接口绑定 ip 失败')
                time.sleep(5)
            # print(self.result)
            return True
        except:
            return False

    # 统一 PUT 请求
    def report_put_json(self, url, data):
        headers = self.curl.headers
        headers = headers.update({
            'Content-Type': 'application/json'
        })
        ret = self.curl.put(url, data=json.dumps(data), headers=headers, timeout=30)
        # print(ret.json())
        self.result = ret.json()
        return True

    # 获取磁盘列表
    def get_disk_list(self):
        url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/providers/Microsoft.Compute/disks?api-version=2020-12-01'
        # self.curl.get(url)
        self.report_get(url)
        for foo in self.result['value']:
            print(foo)

    def get_skus(self):
        url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/providers/Microsoft.Compute/skus?api-version=2019-04-01'
        self.report_get(url)
        for foo in self.result['value']:
            print(foo['name'])

    def get_locations(self):
        url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/locations?api-version=2020-01-01'
        self.report_get(url)
        for foo in self.result['value']:
            print(foo['name'], foo['regionalDisplayName'], foo['displayName'])

    # 创建vm
    def create_vm(self, location = 'eastasia', vm_name = 'cdntip', vm_size = 'Standard_F2s', username = 'cdntip', password='admin7788==', nic_id='', urn='OpenLogic:CentOS:7.5:latest'):
        try:
            urn = urn.split(':')
            url = f'https://management.azure.com/subscriptions/{self.subscriptionId}/resourceGroups/{self.group_name}/providers/Microsoft.Compute/virtualMachines/{vm_name}?api-version=2021-03-01'
            data = {
                "location": location,
                "name": vm_name,
                "properties": {
                    "hardwareProfile": {
                        "vmSize": vm_size
                    },
                    "storageProfile": {
                        "imageReference": {
                            "sku": urn[2],
                            "publisher": urn[0],
                            "version": urn[3],
                            "offer": urn[1]
                        },
                        "osDisk": {
                            "caching": "ReadWrite",
                            "managedDisk": {
                                "storageAccountType": "Premium_LRS"
                            },
                            "name": f"{vm_name}_disk",
                            "diskSizeGB": 64,
                            "createOption": "FromImage"
                        }
                    },
                    "osProfile": {
                        "adminUsername": username,
                        "computerName": f"{vm_name}".replace('_', ''),
                        "adminPassword": password
                    },
                    "networkProfile": {
                        "networkInterfaces": [
                            {
                                "id": nic_id,
                                "properties": {
                                    "primary": True
                                }
                            }
                        ]
                    },
                    "userData": USER_DATA
                }
            }
            self.report_put_json(url, data)
            self.new_vm_info = self.result
            return True
        except:
            return False

    # 统一请求
    def report_get(self, url):
        try:
            ret = self.curl.get(url, timeout=60)
            self.result = ret.json()
            return True
        except BaseException as e:
            print(e)
            return False
# 获取订阅
def get_subscriptions():
    client_id = 'a75b2e32-a18e-4a57-804d-af24eacb35ed'
    client_secret = 'XErlV3sj_prYIjvHNzdMA1hvxrW8k3BXiZ'
    tenant = '433470e8-eb72-4151-b728-12d850b3213e'
    subscriptionId = '7109aa91-e293-437f-904f-67cad2922773'

    azApi = AzureApi(client_id, client_secret, tenant)
    azApi.get_token()
    azApi.get_subscriptions()


def create_vm(client_id, client_secret, tenant, subscriptionId):
    vm_name = 'node_test'

    # 初始化 api
    azApi = AzureApi(client_id, client_secret, tenant)

    # 更新token
    if not azApi.get_token():
        print('获取 access_token 失败')
        return False

    azApi.subscriptionId = subscriptionId

    # 1 创建资源组, 资源组名称统一为 AzureGroup
    group_name = 'AzureGroup'
    location = 'eastasia'

    if not azApi.create_group():
        print('获取 创建资源组失败 失败')
        return False

    # 2, 创建 虚拟网络 和 子网
    vnet_status = azApi.create_virtual_networks(location=location)
    if not vnet_status:
        print('创建 虚拟网络 失败')
        return False

    # 创建子网
    if not azApi.create_subnet(vnet_name=azApi.vnet_name, sub_name=location):
        print('创建 虚拟网络-子网 失败')
        return False

    # 3， 创建公共IP
    if not azApi.create_public_ip(location=location, public_ip_name=vm_name):
        print('创建 公共IP 失败')
        return False

    # 4, 创建网络接口
    if not azApi.create_nic(location=location, nic_name=vm_name, public_ip_id=azApi.public_ip_id, subnet_id=azApi.sub_id):
        print('创建 公共IP 失败')
        return False

    # 5, 创建虚拟机
    if not azApi.create_vm(location=location, vm_name=vm_name, nic_id=azApi.nic_id):
        print('创建 虚拟机 失败')
        return False


if __name__ == '__main__':
   print('Hello CDNTIP!')