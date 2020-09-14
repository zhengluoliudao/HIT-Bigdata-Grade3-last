#ifndef __BITMAP_HPP__
#define __BITMAP_HPP__

#include <cstdlib>
#include <cstring>

class BitMap
{
public:
    BitMap(int min, int max);
    ~BitMap();
    bool set(int value);
    bool clear(int value);
    bool test(int value);
private:
    BitMap(const BitMap &);
    BitMap & operator = (const BitMap &);
private:
    int             m_min;
    int             m_max;
    unsigned char * m_bit;
};

BitMap::BitMap(int min, int max)
 : m_min(min), m_max(max), m_bit(NULL)
{
    int size = (max - min + 8) >> 3;
    m_bit = new unsigned char[size];
    if (m_bit == NULL) {
        abort();
    }
    memset(m_bit, 0, size);
}

BitMap::~BitMap()
{
    delete[] m_bit;
}

bool BitMap::set(int value)
{
    if (value < m_min || value > m_max) {
        return(false);
    }
    value -= m_min;
    m_bit[value >> 3] |= (0x01 << (value & 0x07));
    return(true);
}

bool BitMap::clear(int value)
{
    if (value < m_min || value > m_max) {
        return(false);
    }
    value -= m_min;
    m_bit[value >> 3] &= ~(0x01 << (value & 0x07));
    return(true);
}

bool BitMap::test(int value)
{
    if (value < m_min || value > m_max) {
        return(false);
    }
    value -= m_min;
    return(m_bit[value >> 3] & (0x01 << (value & 0x07)));
}

#endif
