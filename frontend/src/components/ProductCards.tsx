import { Product } from '../services/api'
import './ProductCards.css'

interface ProductCardsProps {
  products: Product[]
}

const ProductCards = ({ products }: ProductCardsProps) => {
  if (!products || products.length === 0) return null

  return (
    <div className="product-cards-container">
      <div className="product-grid">
        {products.map((product, index) => (
          <div key={index} className="product-card">
            <div className="product-header">
              <h3 className="product-brand">{product['Company Name']}</h3>
              <h4 className="product-model">{product['Model Name']}</h4>
            </div>
            <div className="product-price">
              {product['Launched Price (India)'] || product.Price_INR ? (
                <span className="price">
                  {product['Launched Price (India)'] || `₹${product.Price_INR?.toLocaleString('en-IN')}`}
                </span>
              ) : null}
            </div>
            <div className="product-specs">
              {product.Processor && (
                <div className="spec-item">
                  <span className="spec-label">Processor:</span>
                  <span className="spec-value">{product.Processor}</span>
                </div>
              )}
              {product.RAM && (
                <div className="spec-item">
                  <span className="spec-label">RAM:</span>
                  <span className="spec-value">{product.RAM}</span>
                </div>
              )}
              {product['Battery Capacity'] && (
                <div className="spec-item">
                  <span className="spec-label">Battery:</span>
                  <span className="spec-value">{product['Battery Capacity']}</span>
                </div>
              )}
              {product['Back Camera'] && (
                <div className="spec-item">
                  <span className="spec-label">Camera:</span>
                  <span className="spec-value">{product['Back Camera']}</span>
                </div>
              )}
              {product['Screen Size'] && (
                <div className="spec-item">
                  <span className="spec-label">Screen:</span>
                  <span className="spec-value">{product['Screen Size']}</span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ProductCards

