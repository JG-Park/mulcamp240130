import pandas as pd

# 원본 데이터 파일 경로
original_file_path = './input/order_products__train.csv'

# 새로운 데이터 파일 경로
new_file_path = './input/new/order_products__train.csv'

# 랜덤 시드를 설정하여 매번 동일한 샘플을 얻을 수 있도록 함
random_seed = 42

# 원본 데이터 불러오기
df = pd.read_csv(original_file_path)

# 데이터 랜덤 샘플링 (예: 50%의 비율로 샘플링)
sampled_df = df.sample(frac=0.1, random_state=random_seed)

# 샘플링된 데이터를 새로운 파일로 저장
sampled_df.to_csv(new_file_path, index=False)

print(f"New file saved to {new_file_path}")