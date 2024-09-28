--Data Cleaning using SQL

-- Populating the PropertyAddress
--The Values of the PropertyAddress will be filled based on the corresponding Non-values in the same group as ParcelID. And the 
--same ParcelID have same Property Address

Select *
From NashvilleHousing
--where PropertyAddress is null
order by ParcelID 

Select a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress,ISNULL(a.PropertyAddress, b.PropertyAddress)
from NashvilleHousing a
JOIN NashvilleHousing b
ON a.ParcelID = b.ParcelID
AND a.UniqueID <> b.UniqueID
where a.PropertyAddress is null

Update a
SET PropertyAddress = ISNULL(a.PropertyAddress, b.PropertyAddress)
from NashvilleHousing a
JOIN NashvilleHousing b
	ON a.ParcelID = b.ParcelID
	AND a.UniqueID <> b.UniqueID
where a.PropertyAddress is null

--Breaking Address in Individaul columns(Address, City, state)

Select PropertyAddress
from NashvilleHousing

Select 
PARSENAME(REPLACE(PropertyAddress,',', '.'), 2),
PARSENAME(REPLACE(PropertyAddress,',', '.'), 1)
from NashvilleHousing

ALTER TABLE NashvilleHousing
ADD PropertySplitAddress nvarchar(255),
	PropertyAddressCity nvarchar(255); 

UPDATE NashvilleHousing
SET PropertySplitAddress = PARSENAME(REPLACE(PropertyAddress,',', '.'), 2),
	PropertyAddressCity = PARSENAME(REPLACE(PropertyAddress,',', '.'), 1)

select * 
from NashvilleHousing

select OwnerAddress
from NashvilleHousing

Select 
PARSENAME(REPLACE(OwnerAddress,',', '.'), 3),
PARSENAME(REPLACE(OwnerAddress,',', '.'), 2),
PARSENAME(REPLACE(OwnerAddress,',', '.'), 1)
from NashvilleHousing

ALTER TABLE NashvilleHousing
ADD OwnerSplitAddress nvarchar(255),
	OwnerAddressCity nvarchar(255),
	OwnerAddressState nvarchar(255);

UPDATE NashvilleHousing
SET OwnerSplitAddress = PARSENAME(REPLACE(OwnerAddress,',', '.'), 3),
	OwnerAddressCity = PARSENAME(REPLACE(OwnerAddress,',', '.'), 2),
	OwnerAddressState = PARSENAME(REPLACE(OwnerAddress,',', '.'), 1)

select * 
from NashvilleHousing

-- Change Y and N to Yes and No respectively
select Distinct(SoldAsVacant), count(SoldAsVacant)
from NashvilleHousing
Group by SoldAsVacant
order by 2

Select SoldAsVacant,
	CASE when SoldAsVacant = 'N' THEN 'No'
		when SoldAsVacant = 'Y' THEN 'Yes'
		ELSE SoldAsVacant
		END
from NashvilleHousing

Update NashvilleHousing
SET SoldAsVacant = 
	CASE when SoldAsVacant = 'N' THEN 'No'
		when SoldAsVacant = 'Y' THEN 'Yes'
		ELSE SoldAsVacant
		END

-- Removing Duplicates

WITH RowNumCTE AS 
(
	Select *,
	ROW_NUMBER() OVER ( PARTITION BY
	ParcelID,
	PropertyAddress,
	SaleDate,
	SalePrice,
	LegalReference
	order by
	ParcelID
	) AS RowNum
from NashvilleHousing
)

Select *
from RowNumCTE
where RowNum > 1

-- Deleting Unused Column

Select *
From NashvilleHousing

Alter Table NashvilleHousing
Drop Column PropertyAddress, OwnerAddress